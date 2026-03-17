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

    def paginate_queryset(self, queryset):
        if self.request.query_params.get('no_pagination') == 'true':
            return None
        return super().paginate_queryset(queryset)

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

    @action(detail=False, methods=['get'])
    def resumen_movimientos(self, request):
        from django.db.models import Sum
        ingredientes = Ingrediente.objects.all()
        resumen = []
        for ing in ingredientes:
            salidas = ing.movimientos.filter(tipo_movimiento='SALIDA').aggregate(Sum('cantidad'))['cantidad__sum'] or 0
            # El total con el que ingresó = stock actual + salidas
            total_ingreso = float(ing.stock) + float(salidas)
            
            resumen.append({
                'id': ing.id,
                'nombre': ing.nombre_ingrediente,
                'total_ingreso': total_ingreso,
                'total_salida': float(salidas),
                'unidad': ing.unidad_medida,
                'stock_actual': float(ing.stock)
            })
        return Response(resumen)

    @action(detail=False, methods=['post'])
    def registrar_degustacion(self, request):
        """
        Registra una degustación, descontando todos los ingredientes según la receta del producto consumido.
        Body: {producto_id, cantidad, descripcion}
        """
        from productos.models import Producto, Receta
        producto_id = request.data.get('producto_id')
        cantidad = request.data.get('cantidad', 1)
        descripcion = request.data.get('descripcion', 'Degustación empleado')
        usuario = request.user.username if request.user.is_authenticated else "Anonimo"

        if not producto_id:
            return Response({'error': 'Falta el id del producto consumido'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            producto = Producto.objects.get(id=producto_id)
            cantidad = float(cantidad)

            if cantidad <= 0:
                return Response({'error': 'La cantidad debe ser mayor a 0'}, status=status.HTTP_400_BAD_REQUEST)

            recetas = Receta.objects.filter(producto=producto)
            if not recetas.exists():
                return Response({'error': 'El producto no tiene receta definida. No se puede descontar ingredientes de forma automática.'}, status=status.HTTP_400_BAD_REQUEST)

            # Validar que haya stock para todos los ingredientes primero
            for receta in recetas:
                cantidad_requerida = float(receta.cantidad) * cantidad
                if receta.ingrediente.stock < cantidad_requerida:
                    return Response({'error': f'Stock insuficiente para: {receta.ingrediente.nombre_ingrediente}'}, status=status.HTTP_400_BAD_REQUEST)

            # Ejecutar el descuento
            for receta in recetas:
                ingrediente = receta.ingrediente
                cantidad_requerida = float(receta.cantidad) * cantidad
                
                ingrediente.stock = float(ingrediente.stock) - cantidad_requerida
                ingrediente.save()

                # Guardar movimiento individual
                MovimientoInventario.objects.create(
                    ingrediente=ingrediente,
                    tipo_movimiento='SALIDA',
                    cantidad=cantidad_requerida,
                    motivo=f"DEGUSTACIÓN ({cantidad}x {producto.nombre}): {descripcion}",
                    usuario=usuario
                )

            return Response({'message': f'Degustación registrada. Se descontaron {recetas.count()} ingredientes del inventario automáticamente.'}, status=status.HTTP_200_OK)

        except Producto.DoesNotExist:
            return Response({'error': 'Producto no encontrado'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
