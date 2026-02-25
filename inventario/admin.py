from django.contrib import admin
from .models import Ingrediente, MovimientoInventario

@admin.register(Ingrediente)
class IngredienteAdmin(admin.ModelAdmin):
    list_display = ('nombre_ingrediente', 'stock', 'unidad_medida', 'stock_minimo', 'updated_at')
    search_fields = ('nombre_ingrediente',)
    list_filter = ('unidad_medida',)

@admin.register(MovimientoInventario)
class MovimientoInventarioAdmin(admin.ModelAdmin):
    list_display = ('ingrediente', 'tipo_movimiento', 'cantidad', 'motivo', 'fecha', 'usuario')
    list_filter = ('tipo_movimiento', 'fecha')
    search_fields = ('ingrediente__nombre_ingrediente', 'motivo', 'usuario')
    readonly_fields = ('fecha',)
