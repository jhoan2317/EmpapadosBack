import os
import json
import logging
from datetime import datetime
from typing import Dict, Optional
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from django.conf import settings

logger = logging.getLogger(__name__)

class ServiceException(Exception):
    """Excepción base para errores en la capa de servicio."""
    pass

class TokenArchiveService:
    """
    Servicio para archivar tokens antiguos en una carpeta por seguridad.
    """
    ARCHIVE_PATH = os.path.join(settings.BASE_DIR, 'token_archive')

    @classmethod
    def archive_token(cls, user, tokens):
        try:
            if not os.path.exists(cls.ARCHIVE_PATH):
                os.makedirs(cls.ARCHIVE_PATH)
            
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
            filename = f"{user.username}_{timestamp}.json"
            filepath = os.path.join(cls.ARCHIVE_PATH, filename)
            
            data = {
                "username": user.username,
                "timestamp": datetime.now().isoformat(),
                "access": tokens.get("access"),
                "refresh": tokens.get("refresh")
            }
            
            with open(filepath, 'w') as f:
                json.dump(data, f, indent=4)
            logger.info(f"Token archivado correctamente para el usuario '{user.username}'.")
        except Exception as e:
            logger.error(f"Error al archivar el token para '{user.username}': {e}")

class AuthenticationService:
    """
    Lógica para la validación de credenciales de usuario.
    """
    def authenticate(self, username: str, password: str) -> Optional[User]:
        logger.info(f"Servicio de autenticación: Intentando autenticar a '{username}'.")
        user = authenticate(username=username, password=password)
        if not user:
            logger.warning(f"Fallo de autenticación para '{username}'.")
            return None
        logger.info(f"Usuario '{username}' autenticado correctamente.")
        return user

class UserSessionDataService:
    """
    Provee los componentes de datos necesarios para la sesión de un usuario.
    """
    def get_tokens_for_user(self, user: User) -> Dict[str, str]:
        try:
            logger.info(f"Generando tokens JWT para el usuario '{user.username}'.")
            refresh = RefreshToken.for_user(user)
            tokens = {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }
            
            # Guardamos los tokens en la carpeta de archivo por seguridad como se solicitó
            TokenArchiveService.archive_token(user, tokens)
            
            return tokens
        except Exception as e:
            logger.error(f"Error al generar tokens para '{user.username}': {e}", exc_info=True)
            raise ServiceException("No se pudieron generar los tokens de sesión.") from e
