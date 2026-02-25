from rest_framework import viewsets, permissions
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from .models import HeroSection, Feature, Testimonial, GlobalConfig
from .serializers import (
    HeroSectionSerializer, 
    FeatureSerializer, 
    TestimonialSerializer, 
    GlobalConfigSerializer
)

class HeroSectionViewSet(viewsets.ModelViewSet):
    queryset = HeroSection.objects.filter(is_active=True)
    serializer_class = HeroSectionSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

class FeatureViewSet(viewsets.ModelViewSet):
    queryset = Feature.objects.filter(is_active=True)
    serializer_class = FeatureSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

class TestimonialViewSet(viewsets.ModelViewSet):
    queryset = Testimonial.objects.all()
    serializer_class = TestimonialSerializer
    pagination_class = None
    
    def get_permissions(self):
        if self.action == 'create':
            return [permissions.AllowAny()]
        return [IsAuthenticatedOrReadOnly()]

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated or user.is_staff:
            return Testimonial.objects.all().order_by('-id')
        return Testimonial.objects.filter(is_active=True).order_by('-id')

    def perform_create(self, serializer):
        # Si el usuario no está autenticado (es un cliente), el testimonio es inactivo por defecto
        is_authenticated = self.request.user.is_authenticated
        if not is_authenticated:
            testimonial = serializer.save(is_active=False)
        else:
            testimonial = serializer.save()

        # Enviar notificación por WebSocket al administrador
        try:
            channel_layer = get_channel_layer()
            async_to_sync(channel_layer.group_send)(
                "notifications",
                {
                    "type": "send_notification",
                    "notif_type": "new_testimonial", 
                    "message": {
                        "id": testimonial.id,
                        "cliente": testimonial.client_name,
                        "rating": testimonial.rating,
                        "tipo": "comentario"
                    }
                }
            )
        except Exception as e:
            print(f"Error enviando notificación WS: {e}")

class GlobalConfigViewSet(viewsets.ModelViewSet):
    queryset = GlobalConfig.objects.all()
    serializer_class = GlobalConfigSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        # Aseguramos que solo haya una configuración o devolvemos la última
        return GlobalConfig.objects.all()[:1]
