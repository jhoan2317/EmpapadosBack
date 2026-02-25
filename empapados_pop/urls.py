"""
URL configuration for empapados_pop project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework_simplejwt.views import TokenObtainPairView
from .views import AdminLoginView, LogoutAPIView, CustomTokenRefreshView, UserProfileAPIView

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Auth JWT
    path('api/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', CustomTokenRefreshView.as_view(), name='token_refresh'),
    path('api/usuarios/admin-login/', AdminLoginView.as_view(), name='admin_login'),
    path('api/usuarios/logout/', LogoutAPIView.as_view(), name='admin_logout'),
    path('api/usuarios/perfil/', UserProfileAPIView.as_view(), name='user_profile'),

    # APIs
    path("api/productos/", include("productos.urls")),
    path("api/pedidos/", include("pedidos.urls")),
    path("api/inventario/", include("inventario.urls")),
    path("api/reportes/", include("reportes.urls")),
    path("api/galeria/", include("galeria.urls")),
    path("api/pagos/", include("pagos.urls")),
    path("api/marketing/", include("marketing.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
