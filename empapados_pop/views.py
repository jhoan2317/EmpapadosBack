import logging
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError

from .serializers import AuthSerializer
from .services import AuthenticationService, UserSessionDataService, ServiceException
from .authentication import CookieJWTAuthentication

logger = logging.getLogger(__name__)

class CustomTokenRefreshView(TokenRefreshView):
    """
    Vista personalizada para renovar el token leyendo la cookie refresh_token.
    """
    permission_classes = [AllowAny]
    authentication_classes = []

    def post(self, request, *args, **kwargs):
        refresh_token = request.COOKIES.get('refresh_token')
        
        if refresh_token:
            request.data['refresh'] = refresh_token
        
        response = super().post(request, *args, **kwargs)
        
        if response.status_code == 200:
            access_token = response.data.get('access')
            response.set_cookie(
                key="access_token",
                value=access_token,
                httponly=True,
                secure=False,
                samesite="Lax",
                path="/",
                max_age=60 * 60 * 24
            )
        
        return response

class AdminLoginView(APIView):
    """
    Endpoint de la API para la autenticación de administradores.
    Adaptado del código de referencia para usar servicios desacoplados.
    """
    permission_classes = [AllowAny]
    authentication_classes = []

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.auth_service = AuthenticationService()
        self.session_data_service = UserSessionDataService()

    def post(self, request, *args, **kwargs):
        serializer = AuthSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        username = serializer.validated_data['username']
        password = serializer.validated_data['password']

        user = self.auth_service.authenticate(username, password)
        if not user:
            return Response(
                {"detail": "Credenciales inválidas."},
                status=status.HTTP_401_UNAUTHORIZED
            )

        # Mantenemos la restricción de staff si es necesario para el proyecto actual
        if not user.is_staff:
            return Response(
                {"detail": "No tiene permisos de administrador."},
                status=status.HTTP_403_FORBIDDEN
            )

        try:
            tokens = self.session_data_service.get_tokens_for_user(user)
            logger.info(f"Login exitoso para '{username}'.")
            
            response = Response(
                {"detail": "Login exitoso", "username": user.username},
                status=status.HTTP_200_OK
            )

            response.set_cookie(
                key="access_token",
                value=tokens["access"],
                httponly=True,
                secure=False,
                samesite="Lax",
                path="/",
                max_age=60 * 60 * 24
            )

            response.set_cookie(
                key="refresh_token",
                value=tokens["refresh"],
                httponly=True,
                secure=False,
                samesite="Lax",
                path="/",
                max_age=60 * 60 * 24 * 7
            )

            return response

        except ServiceException as e:
            return Response(
                {"detail": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class LogoutAPIView(APIView):
    """
    Cierra sesión invalidando el refresh token y borrando las cookies.
    Se usa AllowAny para que el borrado ocurra incluso si el token ya expiró.
    """
    permission_classes = [AllowAny]

    def post(self, request):
        response = Response(
            {"message": "Sesión cerrada correctamente"},
            status=status.HTTP_200_OK
        )

        refresh_token = request.COOKIES.get("refresh_token")

        if refresh_token:
            try:
                # Intentamos invalidar el token si es posible
                token = RefreshToken(refresh_token)
                token.blacklist()
            except Exception as e:
                # Si falla (token mal formado, etc), solo logeamos
                logger.warning(f"No se pudo invalidar el token durante logout: {str(e)}")

        # Borrar cookies desde el backend (esto funciona para cookies HttpOnly)
        response.delete_cookie(key="access_token", path="/", samesite="Lax")
        response.delete_cookie(key="refresh_token", path="/", samesite="Lax")
        
        # Opcional: borrar otras variantes de nombres por si acaso
        response.delete_cookie(key="accessToken", path="/", samesite="Lax")
        response.delete_cookie(key="refreshToken", path="/", samesite="Lax")

        return response

class UserProfileAPIView(APIView):
    """
    Endpoint para recuperar el perfil del usuario autenticado.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user = request.user
        logger.info(f"Petición de perfil para el usuario '{user.username}'.")

        profile_data = {
            "username": user.username,
            "first_name": user.first_name,
            "email": user.email,
        }
        return Response(profile_data, status=status.HTTP_200_OK)
