from django.db import models


class Pago(models.Model):
    metodo = models.CharField(max_length=50)
    monto = models.DecimalField(max_digits=10, decimal_places=2)
    fecha = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"Pago {self.id} - {self.monto}"


class Gasto(models.Model):

    TIPO_GASTO = (
        ('nomina', 'Nómina'),
        ('proveedor', 'Proveedor'),
        ('servicios', 'Servicios'),
        ('arriendo', 'Arriendo'),
        ('mantenimiento', 'Mantenimiento'),
        ('otros', 'Otros'),
    )

    CARGO_OPCIONES = (
        ('cocinero', 'Cocinero'),
        ('ayudante_cocina', 'Ayudante de Cocina'),
        ('mesero', 'Mesero'),
        ('pizzero', 'Pizzero'),
        ('domiciliario', 'Domiciliario'),
        ('particular', 'Particular'),
    )

    tipo = models.CharField(max_length=20, choices=TIPO_GASTO)
    beneficiario = models.CharField(max_length=150)
    cargo = models.CharField(max_length=50, choices=CARGO_OPCIONES, null=True, blank=True)
    descripcion = models.TextField(blank=True)
    monto = models.DecimalField(max_digits=10, decimal_places=2)
    fecha = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Gasto {self.id} - {self.tipo} - {self.monto}"
