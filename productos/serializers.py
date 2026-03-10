from rest_framework import serializers
from .models import Categoria, Producto, Tamano, ProductoTamano, Receta


class CategoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categoria
        fields = '__all__'

class TamanoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tamano
        fields = '__all__'

class RecetaSerializer(serializers.ModelSerializer):
    ingrediente_nombre = serializers.CharField(source='ingrediente.nombre_ingrediente', read_only=True)
    unidad_medida = serializers.CharField(source='ingrediente.unidad_medida', read_only=True)

    class Meta:
        model = Receta
        fields = ['id', 'producto', 'ingrediente', 'ingrediente_nombre', 'cantidad', 'unidad_medida']

class ProductoSerializer(serializers.ModelSerializer):
    # Permitimos que 'imagen' reciba un string con la URL de Cloudinary
    imagen = serializers.CharField(required=False, allow_null=True)
    categoria_nombre = serializers.CharField(source='categoria.nombre', read_only=True)
    imagen_url = serializers.SerializerMethodField()

    class Meta:
        model = Producto
        fields = [
            'id',
            'nombre',
            'descripcion',
            'imagen',
            'imagen_galeria',
            'imagen_url',
            'categoria',
            'categoria_nombre',
            'precio',
            'es_combo',
            'activo',
            'receta'
        ]
    
    receta = RecetaSerializer(many=True, read_only=True)

    def get_imagen_url(self, obj):
        request = self.context.get('request')
        url = None
        
        # Si ya guardamos una URL completa en el campo imagen
        if obj.imagen and str(obj.imagen).startswith('http'):
            url = str(obj.imagen)
        elif obj.imagen_galeria:
            url = obj.imagen_galeria.imagen.url
        elif obj.imagen:
            url = obj.imagen.url
        
        if url:
            if url.startswith('http') and 'cloudinary.com' in url:
                # Inyectamos optimización automática: formato y calidad automática
                if '/upload/' in url:
                    return url.replace('/upload/', '/upload/f_auto,q_auto/')
                return url
            
            if request:
                return request.build_absolute_uri(url)
            return url
        return None

class ProductoTamanoSerializer(serializers.ModelSerializer):
    producto_id = serializers.PrimaryKeyRelatedField(
        queryset=Producto.objects.all(),
        source='producto',
        write_only=True
    )

    tamano_id = serializers.PrimaryKeyRelatedField(
        queryset=Tamano.objects.all(),
        source='tamano',
        write_only=True
    )

    producto = ProductoSerializer(read_only=True)
    tamano = TamanoSerializer(read_only=True)

    class Meta:
        model = ProductoTamano
        fields = [
            'id',
            'producto',
            'producto_id',
            'tamano',
            'tamano_id',
            'stock'
        ]