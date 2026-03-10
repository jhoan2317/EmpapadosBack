from django.conf import settings
from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from productos.models import Producto, ComboDetalle, Receta
from inventario.models import Ingrediente, MovimientoInventario


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
        if not self.precio_unitario:
            self.precio_unitario = self.producto.precio
        self.subtotal = self.cantidad * self.precio_unitario

        is_new = self.pk is None
        super().save(*args, **kwargs)

        if is_new:
            self.descontar_inventario()

        # Actualizar el total del pedido
        total = sum(d.subtotal for d in self.pedido.detalles.all())
        self.pedido.total = total
        self.pedido.save()

    def descontar_inventario(self):
        """
        Lógica para mermar el inventario basado en la receta del producto.
        """
        # Si es un combo, descontamos los ingredientes de cada producto incluido
        if self.producto.es_combo:
            combos = ComboDetalle.objects.filter(combo=self.producto)
            for item in combos:
                self._procesar_producto_receta(item.producto_incluido, item.cantidad * self.cantidad)
        else:
            self._procesar_producto_receta(self.producto, self.cantidad)

    def _procesar_producto_receta(self, producto, cantidad_pedida):
        recetas = Receta.objects.filter(producto=producto)
        for r in recetas:
            cantidad_a_descontar = r.cantidad * cantidad_pedida
            ingrediente = r.ingrediente
            
            # Actualizar stock
            ingrediente.stock -= cantidad_a_descontar
            ingrediente.save()

            # Registrar movimiento
            MovimientoInventario.objects.create(
                ingrediente=ingrediente,
                tipo_movimiento='SALIDA',
                cantidad=cantidad_a_descontar,
                motivo=f"Venta Automática - Pedido #{self.pedido.id}",
                usuario="Sistema"
            )

    def __str__(self):
        return f"{self.producto.nombre} x {self.cantidad}"
