from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ImagenGaleriaViewSet

router = DefaultRouter()
router.register(r'imagenes', ImagenGaleriaViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
