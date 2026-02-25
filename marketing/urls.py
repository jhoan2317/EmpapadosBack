from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    HeroSectionViewSet, 
    FeatureViewSet, 
    TestimonialViewSet, 
    GlobalConfigViewSet
)

router = DefaultRouter()
router.register(r'hero', HeroSectionViewSet)
router.register(r'features', FeatureViewSet)
router.register(r'testimonials', TestimonialViewSet)
router.register(r'config', GlobalConfigViewSet, basename='config')

urlpatterns = [
    path('', include(router.urls)),
]
