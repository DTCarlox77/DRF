import json
from channels.generic.websocket import AsyncWebsocketConsumer

class NotificacionesConsumer(AsyncWebsocketConsumer):
    
    async def connect(self):
        
        self.user_id = self.scope['url_route']['kwargs']['id']
        self.room_group_name = f'notificaciones_{self.user_id}'
        
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        
        # Acá se autoriza que el usuario pueda acceder al grupo de canal del socket.
        await self.accept()
    
    async def disconnect(self, code):
        
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
        
    # Recepción de información.
    async def receive(self, text_data):
        
        data = json.loads(text_data)
        message = data['message']
        
        await self.channel_layer.group_send(
            self.room_group_name, 
            {
                'type' : 'send_notification',
                'message' : message
            }
        )
        
    async def send_notification(self, event):
        
        message = event['message']
        await self.send(text_data=json.dumps({
            'message' : message
        }))