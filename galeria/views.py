from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .models import ImagenGaleria
from .serializers import ImagenGaleriaSerializer

class ImagenGaleriaViewSet(viewsets.ModelViewSet):
    queryset = ImagenGaleria.objects.all().order_by('-creado_en')
    serializer_class = ImagenGaleriaSerializer
    permission_class_map = {
        'list': [IsAuthenticatedOrReadOnly],
        'retrieve': [IsAuthenticatedOrReadOnly],
        'create': [IsAuthenticatedOrReadOnly], # Permitimos crear solo con sesión o según lógica
        'update': [IsAuthenticatedOrReadOnly],
        'partial_update': [IsAuthenticatedOrReadOnly],
        'destroy': [IsAuthenticatedOrReadOnly],
    }
    # Usamos una versión más simple directamente para evitar problemas de importación
    permission_classes = [IsAuthenticatedOrReadOnly]
