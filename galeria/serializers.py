from rest_framework import serializers
from .models import ImagenGaleria

class ImagenGaleriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImagenGaleria
        fields = '__all__'
