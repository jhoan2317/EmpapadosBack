from django.db import models

class Categoria(models.Model):
    nombre = models.CharField(max_length=100)
    activa = models.BooleanField(default=True)

    def __str__(self):
        return self.nombre
    
class Tamano(models.Model):
    nombre = models.CharField(max_length=50)

    def __str__(self):
        return self.nombre

class Producto(models.Model):
    nombre = models.CharField(max_length=150)
    descripcion = models.TextField(blank=True, null=True)
    imagen = models.ImageField(upload_to='productos/', blank=True, null=True)
    imagen_galeria = models.ForeignKey('galeria.ImagenGaleria', on_delete=models.SET_NULL, null=True, blank=True)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    precio = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    es_combo = models.BooleanField(default=False)
    activo = models.BooleanField(default=True)
    creado_en = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nombre

class ProductoTamano(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    tamano = models.ForeignKey(Tamano, on_delete=models.CASCADE)
    stock = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.producto.nombre} - {self.tamano.nombre}"

class ComboDetalle(models.Model):
    combo = models.ForeignKey(Producto, on_delete=models.CASCADE, related_name='combo_principal')
    producto_incluido = models.ForeignKey(Producto, on_delete=models.CASCADE, related_name='productos_incluidos')
    cantidad = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.combo.nombre} incluye {self.producto_incluido.nombre}"    
    