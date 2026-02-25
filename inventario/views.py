from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Ingrediente, MovimientoInventario
from .serializers import IngredienteSerializer, MovimientoInventarioSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny

from rest_framework.pagination import PageNumberPagination

class SmallResultSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

class MovimientoInventarioViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = MovimientoInventario.objects.all().order_by('-fecha')
    serializer_class = MovimientoInventarioSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = SmallResultSetPagination

class IngredienteViewSet(viewsets.ModelViewSet):
    queryset = Ingrediente.objects.all()
    serializer_class = IngredienteSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = SmallResultSetPagination

    @action(detail=False, methods=['post'])
    def registrar_salida(self, request):
        """
        Registra una salida de inventario y actualiza el stock
        Body: {ingrediente_id, cantidad, motivo, usuario}
        """
        ingrediente_id = request.data.get('ingrediente_id')
        cantidad = request.data.get('cantidad')
        motivo = request.data.get('motivo', 'Salida normal')
        usuario = request.user.username if request.user.is_authenticated else "Anonimo"

        if not ingrediente_id or not cantidad:
            return Response({'error': 'Faltan datos requeridos (ingrediente_id, cantidad)'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            ingrediente = Ingrediente.objects.get(id=ingrediente_id)
            cantidad = float(cantidad)

            if cantidad <= 0:
                return Response({'error': 'La cantidad debe ser mayor a 0'}, status=status.HTTP_400_BAD_REQUEST)
            
            if ingrediente.stock < cantidad:
                return Response({'error': 'Stock insuficiente'}, status=status.HTTP_400_BAD_REQUEST)

             # Actualizar stock
            ingrediente.stock = float(ingrediente.stock) - cantidad
            ingrediente.save()

            # Guardar movimiento
            MovimientoInventario.objects.create(
                ingrediente=ingrediente,
                tipo_movimiento='SALIDA',
                cantidad=cantidad,
                motivo=motivo,
                usuario=usuario
            )

            return Response({'message': 'Salida registrada correctamente', 'nuevo_stock': ingrediente.stock}, status=status.HTTP_200_OK)

        except Ingrediente.DoesNotExist:
            return Response({'error': 'Ingrediente no encontrado'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
