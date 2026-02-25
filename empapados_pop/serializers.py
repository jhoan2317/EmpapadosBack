from rest_framework import serializers

class AuthSerializer(serializers.Serializer):
    """
    Serializer para validar el formato de las credenciales de entrada.
    """
    username = serializers.CharField(max_length=150)
    password = serializers.CharField(style={'input_type': 'password'}, trim_whitespace=False)
