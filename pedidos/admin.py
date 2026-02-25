from django.contrib import admin
from .models import Pedido, DetallePedido

class DetallePedidoInline(admin.TabularInline):
    model = DetallePedido
    extra = 1

@admin.register(Pedido)
class PedidoAdmin(admin.ModelAdmin):
    list_display = (
        'id', 
        'nombre_cliente',
        'telefono', 
        'estado', 
        'tipo_pedido', 
        'metodo_pago', 
        'fecha', 
        'total'
    )
    list_filter = ('estado', 'tipo_pedido', 'fecha', 'metodo_pago')
    search_fields = ('nombre_cliente', 'telefono')
    inlines = [DetallePedidoInline]    

@admin.register(DetallePedido)
class DetallePedidoAdmin(admin.ModelAdmin):
    list_display = ('pedido', 'producto', 'cantidad', 'subtotal')    
