from django.db.models.signals import post_save
from django.dispatch import receiver
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from .models import Pedido

@receiver(post_save, sender=Pedido)
def notify_new_order(sender, instance, created, **kwargs):
    # Se envía solo si es un pedido nuevo y aún no ha sido notificado.
    # Usamos instance._notified como bandera temporal en el ciclo de vida del objeto.
    if instance.estado == 'pendiente' and instance.total > 0 and not getattr(instance, '_notified', False):
        channel_layer = get_channel_layer()
        if channel_layer:
            async_to_sync(channel_layer.group_send)(
                "notifications",
                {
                    "type": "send_notification",
                    "notif_type": "new_order",
                    "message": {
                        "id": instance.id,
                        "cliente": instance.nombre_cliente,
                        "tipo": instance.tipo_pedido,
                        "total": str(instance.total),
                        "timestamp": instance.fecha.isoformat()
                    }
                }
            )
            # Marcamos como notificado para esta instancia en memoria
            instance._notified = True
