from rest_framework import serializers
from .models import Pedido, DetallePedido
from productos.models import Producto

class DetallePedidoSerializer(serializers.ModelSerializer):
    producto_nombre = serializers.CharField(source='producto.nombre', read_only=True)
    
    class Meta:
        model = DetallePedido
        fields = ['producto', 'producto_nombre', 'cantidad', 'precio_unitario', 'subtotal']
        read_only_fields = ['precio_unitario', 'subtotal']

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
            precio = producto.precio

            subtotal = precio * cantidad
            total += subtotal

            DetallePedido.objects.create(
                pedido=pedido,
                producto=producto,
                cantidad=cantidad,
                precio_unitario=precio,
                subtotal=subtotal
            )

        pedido.total = total
        pedido.save()
        return pedido

# SERIALIZER DEL ADMIN 
class PedidoAdminSerializer(serializers.ModelSerializer):
    detalles = DetallePedidoSerializer(many=True, read_only=True)

    class Meta:
        model = Pedido
        fields = '__all__'