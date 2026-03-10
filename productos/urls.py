from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (CategoriaViewSet, ProductoViewSet, TamanoViewSet, ProductoTamanoViewSet, RecetaViewSet)

app_name = 'local_productos'
api_version = "api/v01/"


router = DefaultRouter()
router.register(r'categorias', CategoriaViewSet, basename='app_categorias_api')
router.register(r'productos', ProductoViewSet, basename='app_productos_api')
router.register(r'recetas', RecetaViewSet, basename='app_recetas_api')

urlpatterns = router.urls