import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from channels.security.websocket import AllowedHostsOriginValidator
from django.urls import path
from empapados_pop.consumers import NotificationConsumer

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'empapados_pop.settings')

# Obtenemos la aplicación ASGI de Django para manejar el tráfico HTTP
django_asgi_app = get_asgi_application()

application = ProtocolTypeRouter({
    # Tráfico web normal
    "http": django_asgi_app,
    
    # Tráfico de tiempo real (WebSockets)
    "websocket": AllowedHostsOriginValidator(
        AuthMiddlewareStack(
            URLRouter([
                path("ws/notifications/", NotificationConsumer.as_asgi()),
            ])
        )
    ),
})
