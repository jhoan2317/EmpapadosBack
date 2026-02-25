from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from .models import Categoria, Producto, Tamano, ProductoTamano
from .serializers import (
    CategoriaSerializer, 
    ProductoSerializer, 
    TamanoSerializer, 
    ProductoTamanoSerializer
)
from rest_framework.renderers import JSONRenderer
from django.http import JsonResponse
from rest_framework.response import Response


from rest_framework.pagination import PageNumberPagination

class SmallResultSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

#Api publica (solo lectura)
class CategoriaViewSet(viewsets.ModelViewSet):
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    renderer_classes = [JSONRenderer]
    pagination_class = None
class ProductoViewSet(viewsets.ModelViewSet):
    queryset = Producto.objects.all()
    serializer_class = ProductoSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    renderer_classes = [JSONRenderer]
    pagination_class = SmallResultSetPagination

    def paginate_queryset(self, queryset):
        if self.request.query_params.get('no_pagination') == 'true':
            return None
        return super().paginate_queryset(queryset)

#api admin (crud completo)
class TamanoViewSet(viewsets.ModelViewSet):
    queryset = Tamano.objects.all()
    serializer_class = TamanoSerializer
    permission_classes = [IsAuthenticated]

class ProductoTamanoViewSet(viewsets.ModelViewSet):
    queryset = ProductoTamano.objects.all()
    serializer_class = ProductoTamanoSerializer
    permission_classes = [IsAuthenticated]            
