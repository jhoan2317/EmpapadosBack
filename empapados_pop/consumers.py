import json
from channels.generic.websocket import AsyncWebsocketConsumer

class NotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.group_name = "notifications"
        
        # Unirse al grupo de notificaciones
        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        # Salir del grupo
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )

    # Recibir mensaje del grupo
    async def send_notification(self, event):
        message = event['message']
        # El campo 'type' es usado por Channels para el método, 
        # así que usamos 'notif_type' para el tipo de alerta real.
        notif_type = event.get('notif_type', 'new_order')
        
        # Enviar mensaje al WebSocket
        await self.send(text_data=json.dumps({
            'type': notif_type,
            'message': message
        }))
