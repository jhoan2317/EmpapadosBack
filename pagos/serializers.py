from rest_framework import serializers
from .models import Pago, Gasto


class PagoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pago
        fields = "__all__"


class GastoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Gasto
        fields = "__all__"
