from django.shortcuts import redirect
from django.urls import resolve, Resolver404
import logging

logger = logging.getLogger(__name__)

class Redirect404IfNotAuthenticatedMiddleware:
    """
    Middleware que redirige a los usuarios no autenticados a la página de login
    cuando intentan acceder a rutas que no son de la API ni la propia página de login.
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Permitir siempre las peticiones a la API y a la ruta de login
        # Adaptamos las rutas según el proyecto actual
        if not request.user.is_authenticated:
            path = request.path
            # Permitir API, Admin, Login y WebSockets
            if not any(x in path for x in ['/api/', '/admin/', '/login/', '/ws/']):
                return redirect('/login/') # O la ruta de login que elijas

        try:
            resolve(request.path)
        except Resolver404:
            if not request.user.is_authenticated:
                return redirect('/login/')
                
        return self.get_response(request)
