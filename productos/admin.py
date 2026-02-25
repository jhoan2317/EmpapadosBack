from django.contrib import admin
from .models import Categoria, Tamano, Producto, ProductoTamano, ComboDetalle

admin.site.register(Categoria)
admin.site.register(Tamano)
admin.site.register(Producto)
admin.site.register(ProductoTamano)
admin.site.register(ComboDetalle)
