import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.exceptions import StopConsumer
# https://www.youtube.com/watch?v=sthCUcw5Zog

class NotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user = self.scope['user']
        self.room_group_name = 'notifications_%s' % self.user.username

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()
        
    async def disconnect(self, event):
        await self.channel_layer.group_discard(self.group.name, self.channel_name)
        raise StopConsumer()
    
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'notification',
                'message': message
            }
        )
    async def notification(self, event):
        message = event['message']

        #Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message,
            'type': 'notification'
        }))