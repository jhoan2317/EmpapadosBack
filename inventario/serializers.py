from rest_framework import serializers
from .models import Ingrediente, MovimientoInventario

class IngredienteSerializer(serializers.ModelSerializer):
    categoria_nombre = serializers.CharField(source='categoria.nombre', read_only=True)

    class Meta:
        model = Ingrediente
        fields = ['id', 'nombre_ingrediente', 'categoria', 'categoria_nombre', 'stock', 'stock_minimo', 'unidad_medida']

class MovimientoInventarioSerializer(serializers.ModelSerializer):
    nombre_ingrediente = serializers.SerializerMethodField()

    def get_nombre_ingrediente(self, obj):
        return obj.ingrediente.nombre_ingrediente

    class Meta:
        model = MovimientoInventario
        fields = ['id', 'ingrediente', 'nombre_ingrediente', 'tipo_movimiento', 'cantidad', 'motivo', 'fecha', 'usuario']
