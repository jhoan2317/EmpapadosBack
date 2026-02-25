from django.conf import settings
from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from productos.models import Producto


class Pedido(models.Model):

    TIPOS_PEDIDO = [
        ('domicilio', 'Domicilio'),
        ('local', 'Consumo local'),
    ]

    METODO_PAGO = [
        ('efectivo', 'Efectivo'),
        ('nequi', 'Nequi'),
        ('contra_entrega', 'Contra Entrega'),
        ('transferencia', 'Transferencia'),
    ]

    ESTADOS = [
        ('pendiente', 'Pendiente'),
        ('procesando', 'Procesando'),
        ('enviado', 'Enviado'),
        ('entregado', 'Entregado'),
        ('cancelado', 'Cancelado'),
        ('pagado', 'Pagado'),  # necesario para integrar pagos
    ]

    # Datos del cliente (sin login)
    nombre_cliente = models.CharField(max_length=150)
    telefono = models.CharField(max_length=20)

    tipo_pedido = models.CharField(max_length=20, choices=TIPOS_PEDIDO)
    direccion = models.CharField(max_length=255, blank=True, null=True)
    numero_mesa = models.PositiveIntegerField(blank=True, null=True)

    metodo_pago = models.CharField(max_length=20, choices=METODO_PAGO)
    estado = models.CharField(max_length=20, choices=ESTADOS, default='pendiente')
    fecha = models.DateTimeField(auto_now_add=True)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    observaciones = models.TextField(blank=True, null=True)

    def clean(self):
        if self.tipo_pedido == 'local' and self.numero_mesa is None:
            raise ValidationError("Los pedidos en local requieren número de mesa.")

        if self.tipo_pedido == 'domicilio' and not self.direccion:
            raise ValidationError("Los pedidos a domicilio requieren dirección.")

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Pedido #{self.id} - {self.nombre_cliente}"


class DetallePedido(models.Model):
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE, related_name='detalles')
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField()
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)


    def clean(self):
        if self.cantidad <= 0:
            raise ValidationError("La cantidad debe ser mayor que cero.")

    def save(self, *args, **kwargs):
        self.precio_unitario = self.producto.precio
        self.subtotal = self.cantidad * self.precio_unitario

        super().save(*args, **kwargs)

        total = sum(d.subtotal for d in self.pedido.detalles.all())
        self.pedido.total = total
        self.pedido.save()

    def __str__(self):
        return f"{self.producto.nombre} x {self.cantidad}"
