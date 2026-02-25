from rest_framework_simplejwt.authentication import JWTAuthentication

class CookieJWTAuthentication(JWTAuthentication):
    """
    Extensión de JWTAuthentication para soportar la lectura de tokens desde cookies HTTPOnly.
    Se separa en este archivo para evitar importaciones circulares en el arranque de Django.
    """
    def authenticate(self, request):
        # Intentamos obtener el access_token de la cookie
        access_token = request.COOKIES.get('access_token')
        
        if access_token:
            try:
                validated_token = self.get_validated_token(access_token)
                return self.get_user(validated_token), validated_token
            except:
                return None
        
        # Si no hay cookie, permitimos que siga el flujo normal (Header Authorization)
        return super().authenticate(request)
