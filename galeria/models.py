from django.db import models

class ImagenGaleria(models.Model):
    titulo = models.CharField(max_length=150, blank=True, null=True)
    imagen = models.ImageField(upload_to='galeria/')
    creado_en = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.titulo or f"Imagen {self.id}"
