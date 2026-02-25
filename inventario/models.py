from django.db import models

class Ingrediente(models.Model):
    UNIDADES = [
        ('unidades', 'Unidades'),
        ('kg', 'Kilogramos'),
        ('g', 'Gramos'),
        ('l', 'Litros'),
        ('ml', 'Mililitros'),
    ]

    nombre_ingrediente = models.CharField(max_length=150, unique=True)
    stock = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    stock_minimo = models.DecimalField(max_digits=10, decimal_places=2, default=5.00)
    unidad_medida = models.CharField(max_length=20, choices=UNIDADES, default='unidades')
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.nombre_ingrediente} ({self.stock} {self.unidad_medida})"

class MovimientoInventario(models.Model):
    TIPO_MOVIMIENTO = [
        ('ENTRADA', 'Entrada'),
        ('SALIDA', 'Salida'),
        ('AJUSTE', 'Ajuste'),
    ]

    ingrediente = models.ForeignKey(Ingrediente, related_name='movimientos', on_delete=models.CASCADE)
    tipo_movimiento = models.CharField(max_length=10, choices=TIPO_MOVIMIENTO)
    cantidad = models.DecimalField(max_digits=10, decimal_places=2)
    motivo = models.CharField(max_length=255, blank=True, null=True)
    fecha = models.DateTimeField(auto_now_add=True)
    usuario = models.CharField(max_length=150, blank=True, null=True) # O ForeignKey a User si tienes AUTH

    def __str__(self):
        return f"{self.tipo_movimiento} - {self.ingrediente.nombre_ingrediente} - {self.cantidad}"
