from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import Pedido
from .serializers import PedidoAdminSerializer, PedidoSerializer
from .permissions import IsAdminUserCustom
from rest_framework.renderers import JSONRenderer


from rest_framework.pagination import PageNumberPagination

class SmallResultSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

class PedidoViewSet(viewsets.ModelViewSet):
    queryset = Pedido.objects.all().order_by('-id')
    renderer_classes = [JSONRenderer]
    pagination_class = SmallResultSetPagination
    
    def get_queryset(self):
        queryset = Pedido.objects.all().order_by('-id')
        fecha = self.request.query_params.get('fecha', None)
        tipo = self.request.query_params.get('tipo', None)
        estado = self.request.query_params.get('estado', None)
        
        if fecha:
            queryset = queryset.filter(fecha__date=fecha)
        if tipo and tipo != 'todas':
            queryset = queryset.filter(tipo_pedido=tipo)
        if estado:
            queryset = queryset.filter(estado=estado)
            
        return queryset
    
    def get_serializer_class(self):
        if self.action == 'create':
            return PedidoSerializer
        return PedidoAdminSerializer
    
    def get_permissions(self):
        if self.action == 'create':
            return [AllowAny()]
        return [IsAdminUserCustom()]

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        
        # Calculamos el puesto (pedidos pendientes o en proceso)
        # Excluimos el pedido actual de la cuenta para decir "estás en el puesto X"
        puesto = Pedido.objects.filter(estado__in=['pendiente', 'procesando']).count()
        
        # Tiempo estimado: 15 minutos por pedido en cola
        demora = puesto * 15 if puesto > 0 else 15
        
        response.data['puesto'] = puesto
        response.data['demora'] = demora
        
        return response

    def perform_create(self, serializer):
        serializer.save()