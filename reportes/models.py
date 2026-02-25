from django.db import models

TIPO_REPORTE = (
    ('ventas', 'Ventas'),
    ('inventario', 'Inventario'),
    ('movimientos', 'Movimientos'),
)

class Reporte(models.Model):
    tipo = models.CharField(max_length=20, choices=TIPO_REPORTE)
    fecha_generacion = models.DateTimeField(auto_now_add=True)
    descripcion = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Reporte {self.tipo} - {self.fecha_generacion}"
