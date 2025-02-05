import json

from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist

from .models import Message, Room


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_id = self.scope['url_route']['kwargs']['chat_id']
        self.room_group_name = f'room_{self.room_id}'

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()
        await self.send_system_message(f'{self.scope["user"].username} присоединился к чату.')

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

        await self.send_system_message(f'{self.scope["user"].username} покинул чат.')

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        username = self.scope["user"].username
        
        user = self.scope["user"]
        chat = await self.get_chat()
        if not chat:
            print("Чат не найден.")
            return

        if username == 'System':
            return

        await self.save_message(chat, user, message)

        created_at = timezone.localtime(timezone.now()).strftime('%Y %b %d %H:%M')
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'username': username,
                'created_at': created_at,
            }
        )

    async def chat_message(self, event):
        message = event['message']
        username = event.get('username', 'System')
        created_at = event.get('created_at')

        await self.send(text_data=json.dumps({
            'message': f'({created_at}) {username}: {message}',
        }))

    @database_sync_to_async
    def get_chat(self):
        try:
            return Room.objects.get(id=self.room_id)
        except ObjectDoesNotExist:
            print("Chat not found.")
            return None

    @database_sync_to_async
    def save_message(self, room, user, text):
        return Message.objects.create(
            room=room,
            user=user,
            text=text,
            created_at = timezone.now()
        )
    
    async def send_system_message(self, message, username='System'):
        created_at = timezone.localtime(timezone.now()).strftime('%H:%M')
        
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'username': username,
                'created_at': created_at,
            }
        )
        