from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

class HeroSection(models.Model):
    title = models.CharField(max_length=200, verbose_name="Título Principal")
    subtitle = models.TextField(verbose_name="Subtítulo/Descripción")
    image = models.ImageField(upload_to='marketing/hero/', blank=True, null=True, verbose_name="Imagen de Fondo")
    image_url = models.URLField(max_length=500, blank=True, null=True, verbose_name="URL Imagen Externa (Cloudinary)")
    button_text = models.CharField(max_length=50, default="Comprar ahora", verbose_name="Texto del Botón")
    button_link = models.CharField(max_length=200, default="/order", verbose_name="Enlace del Botón")
    is_active = models.BooleanField(default=True, verbose_name="¿Está activo?")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Sección Hero"
        verbose_name_plural = "Secciones Hero"

    def __str__(self):
        return self.title

class Feature(models.Model):
    title = models.CharField(max_length=100, verbose_name="Título del Servicio")
    description = models.TextField(verbose_name="Descripción")
    icon = models.CharField(max_length=50, default="bi-star", verbose_name="Icono (Clase Bootstrap Icons)")
    image = models.ImageField(upload_to='marketing/features/', blank=True, null=True, verbose_name="Imagen (Opcional)")
    image_url = models.URLField(max_length=500, blank=True, null=True, verbose_name="URL Imagen Externa")
    order = models.PositiveIntegerField(default=0, verbose_name="Orden de visualización")
    is_active = models.BooleanField(default=True, verbose_name="¿Está activo?")

    class Meta:
        verbose_name = "Servicio/Feature"
        verbose_name_plural = "Servicios/Features"
        ordering = ['order']

    def __str__(self):
        return self.title

class Testimonial(models.Model):
    client_name = models.CharField(max_length=100, verbose_name="Nombre del Cliente")
    client_role = models.CharField(max_length=100, blank=True, null=True, verbose_name="Cargo/Rol (Opcional)")
    content = models.TextField(verbose_name="Testimonio")
    rating = models.PositiveIntegerField(
        default=5, 
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        verbose_name="Calificación (1-5)"
    )
    image = models.ImageField(upload_to='marketing/testimonials/', blank=True, null=True, verbose_name="Foto del Cliente")
    image_url = models.URLField(max_length=500, blank=True, null=True, verbose_name="URL Foto Externa")
    is_active = models.BooleanField(default=True, verbose_name="¿Está activo?")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Testimonio"
        verbose_name_plural = "Testimonios"

    def __str__(self):
        return f"{self.client_name} - {self.rating} estrellas"

class GlobalConfig(models.Model):
    site_name = models.CharField(max_length=100, default="Empapados Pop")
    contact_whatsapp = models.CharField(max_length=20, blank=True, null=True)
    contact_phone = models.CharField(max_length=20, blank=True, null=True)
    contact_email = models.EmailField(blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    instagram_url = models.URLField(blank=True, null=True)
    facebook_url = models.URLField(blank=True, null=True)
    footer_text = models.TextField(blank=True, null=True, default="© 2024 Empapados Pop. Todos los derechos reservados.")
    
    # Horarios de atención
    opening_hours = models.TextField(blank=True, null=True, verbose_name="Horarios de Atención")

    class Meta:
        verbose_name = "Configuración Global"
        verbose_name_plural = "Configuración Global"

    def __str__(self):
        return "Configuración del Sitio"
