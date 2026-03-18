from rest_framework import serializers
from .models import Pedido, DetallePedido
from productos.models import Producto

class DetallePedidoSerializer(serializers.ModelSerializer):
    producto_nombre = serializers.CharField(source='producto.nombre', read_only=True)
    precio_unitario = serializers.DecimalField(max_digits=10, decimal_places=2, required=False)
    swaps = serializers.DictField(child=serializers.IntegerField(), required=False, write_only=True)
    additions_data = serializers.ListField(child=serializers.IntegerField(), required=False, write_only=True)
    
    class Meta:
        model = DetallePedido
        fields = ['producto', 'producto_nombre', 'cantidad', 'precio_unitario', 'subtotal', 'swaps', 'additions_data']
        read_only_fields = ['subtotal']

class PedidoSerializer(serializers.ModelSerializer):
    detalles = DetallePedidoSerializer(many=True)

    class Meta:
        model = Pedido
        fields = [
            'id',
            'nombre_cliente',
            'telefono',
            'tipo_pedido',
            'direccion',
            'numero_mesa',
            'metodo_pago',
            'estado',
            'total',
            'observaciones',
            'detalles'
        ]
        read_only_fields = ['estado', 'total']

    def validate(self, data):
        tipo = data.get('tipo_pedido')
        direccion = data.get('direccion')
        numero_mesa = data.get('numero_mesa')

        if tipo == 'local' and numero_mesa is None:
            raise serializers.ValidationError(
                {"numero_mesa": "Debe especificar número de mesa para consumo local."}
            )

        if tipo == 'domicilio' and not direccion:
            raise serializers.ValidationError(
                {"direccion": "Debe especificar una dirección para domicilio."}
            )

        return data

    def create(self, validated_data):
        detalles_data = validated_data.pop('detalles')
        pedido = Pedido.objects.create(**validated_data)
        total = 0

        for item in detalles_data:
            producto = item['producto']
            cantidad = item['cantidad']
            precio = item.get('precio_unitario', producto.precio)
            swaps = item.get('swaps', {})
            additions = item.get('additions_data', [])

            subtotal = precio * cantidad
            total += subtotal

            detalle = DetallePedido(
                pedido=pedido,
                producto=producto,
                cantidad=cantidad,
                precio_unitario=precio,
                subtotal=subtotal
            )
            
            # Guardamos la info temporalmente en la instancia para usarla luego en el save del modelo
            setattr(detalle, '_swaps_temp', swaps)
            setattr(detalle, '_additions_temp', additions)
            detalle.save()

        pedido.total = total
        pedido.save()
        return pedido

# SERIALIZER DEL ADMIN 
class PedidoAdminSerializer(serializers.ModelSerializer):
    detalles = DetallePedidoSerializer(many=True, required=False)

    class Meta:
        model = Pedido
        fields = '__all__'

    def update(self, instance, validated_data):
        detalles_data = validated_data.pop('detalles', None)
        
        # Actualizar campos regulares del pedido
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
            
        # Si se envían nuevos detalles, reemplazamos los anteriores
        if detalles_data is not None:
            instance.detalles.all().delete()
            total = 0
            
            for item in detalles_data:
                producto = item['producto']
                cantidad = item['cantidad']
                precio = item.get('precio_unitario', producto.precio)
                swaps = item.get('swaps', {})
                additions = item.get('additions_data', [])

                subtotal = precio * cantidad
                total += subtotal

                detalle = DetallePedido(
                    pedido=instance,
                    producto=producto,
                    cantidad=cantidad,
                    precio_unitario=precio,
                    subtotal=subtotal
                )
                setattr(detalle, '_swaps_temp', swaps)
                setattr(detalle, '_additions_temp', additions)
                detalle.save()
                
            instance.total = total
            
        instance.save()
        return instance