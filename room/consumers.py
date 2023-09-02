import json
from django.contrib.auth.models import User
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async
from .models import Room, Message


class ChatConsumer(AsyncWebsocketConsumer):
    online_users = {}  # Dictionary to store online users

    # WebSocket connection established
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name

        # Add this channel to the group associated with the chat room
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        # Accept the WebSocket connection
        await self.accept()

        # Add the user to the chat room
        await self.add_user_to_room()

    # WebSocket connection closed
    async def disconnect(self, code):
        # Remove the user from the chat room
        await self.remove_user_from_room()

        # Remove this channel from the group associated with the chat room
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Add the user to the chat room
    async def add_user_to_room(self):
        user = self.scope['user']
        room = await self.get_room_object()
        await self.add_user_to_online_participants(room, user)

        # Notify clients about updated participants list
        await self.send_updated_participants_list()

    # Remove the user from the chat room
    async def remove_user_from_room(self):
        user = self.scope['user']
        room = await self.get_room_object()
        await self.remove_user_from_online_participants(room, user)

        # Notify clients about updated participants list
        await self.send_updated_participants_list()

    # Send updated list of online participants to user
    async def send_updated_participants_list(self):
        room = await self.get_room_object()
        online_participants = await self.get_online_participants(room)
        total_online_users = len(online_participants)

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'online_users',
                'online_users': online_participants,
                'total_online_users': total_online_users,
            }
        )

    # Fetch the room object based on the room name
    @sync_to_async
    def get_room_object(self):
        return Room.objects.get(slug=self.room_name)

    # Add a user to the list of online participants in a room
    @sync_to_async
    def add_user_to_online_participants(self, room, user):
        room.online_participants.add(user)

    # Remove a user from the list of online participants in a room
    @sync_to_async
    def remove_user_from_online_participants(self, room, user):
        room.online_participants.remove(user)

    # Get a list of online participants in a room
    @sync_to_async
    def get_online_participants(self, room):
        return list(room.online_participants.values_list('username', flat=True))

    # Handle user status changes (online)
    async def user_status(self, event):
        await self.send(text_data=json.dumps({
            'username': event['username'],
            'status': event['status']
        }))

    # Send information about online users to clients
    async def online_users(self, event):
        online_users = event['online_users']
        total_online_users = event['total_online_users']

        await self.send(text_data=json.dumps({
            'online_users': online_users,
            'total_online_users': total_online_users,
        }))

    # Receive and handle messages from clients
    async def receive(self, text_data):
        data = json.loads(text_data)
        print(data)
        message = data['message']
        username = data['username']
        room = data['room']

        # Save the message to the database
        await self.save_message(username, room, message)

        # Broadcast the message to all users in the room
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'username': username
            }
        )

    # Handle and send chat messages to users
    async def chat_message(self, event):
        message = event['message']
        username = event['username']

        await self.send(text_data=json.dumps({
            'message': message,
            'username': username
        }))

    # Save chat messages to the database
    @sync_to_async
    def save_message(self, username, room, message):
        user = User.objects.get(username=username)
        room = Room.objects.get(slug=room)

        Message.objects.create(user=user, room=room, content=message)
