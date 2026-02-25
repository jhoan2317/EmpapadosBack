from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import IngredienteViewSet, MovimientoInventarioViewSet

router = DefaultRouter()
router.register(r'inventario', IngredienteViewSet, basename='inventario')
router.register(r'movimientos', MovimientoInventarioViewSet, basename='movimientos')

urlpatterns = [
    path('', include(router.urls)),
]
