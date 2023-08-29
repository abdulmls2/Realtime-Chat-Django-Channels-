import json

from django.contrib.auth.models import User
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async

from .models import Room, Message

class ChatConsumer(AsyncWebsocketConsumer):
    online_users = {}  # Dictionary to store online users

    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()
        print('user logged in')
        await self.add_user_to_room()

    async def disconnect(self, code):
        print('user offline')
        await self.remove_user_from_room()

        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def add_user_to_room(self):
        user = self.scope['user']
        room = await self.get_room_object()
        await self.add_user_to_online_participants(room, user)

        await self.send_updated_participants_list()

    async def remove_user_from_room(self):
        user = self.scope['user']
        room = await self.get_room_object()
        await self.remove_user_from_online_participants(room, user)

        await self.send_updated_participants_list()

    async def send_updated_participants_list(self):
        room = await self.get_room_object()
        online_participants = await self.get_online_participants(room)

        print(f"Online users in room '{room.name}': {', '.join(online_participants)}")

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'online_users',
                'online_users': online_participants
            }
        )

    @sync_to_async
    def get_room_object(self):
        return Room.objects.get(slug=self.room_name)

    @sync_to_async
    def add_user_to_online_participants(self, room, user):
        room.online_participants.add(user)

    @sync_to_async
    def remove_user_from_online_participants(self, room, user):
        room.online_participants.remove(user)

    @sync_to_async
    def get_online_participants(self, room):
        return list(room.online_participants.values_list('username', flat=True))

    async def user_status(self, event):
        await self.send(text_data=json.dumps({
            'username': event['username'],
            'status': event['status']
        }))

    async def online_users(self, event):
        online_users = event['online_users']

        await self.send(text_data=json.dumps({
            'online_users': online_users
        }))

    async def receive(self, text_data):
        data = json.loads(text_data)
        print(data)
        message = data['message']
        username = data['username']
        room = data['room']

        await self.save_message(username, room, message)

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'username': username
            }
        )

    async def chat_message(self, event):
        message = event['message']
        username = event['username']

        await self.send(text_data=json.dumps({
            'message': message,
            'username': username
        }))

    @sync_to_async
    def save_message(self, username, room, message):
        user = User.objects.get(username=username)
        room = Room.objects.get(slug=room)

        Message.objects.create(user=user, room=room, content=message)
