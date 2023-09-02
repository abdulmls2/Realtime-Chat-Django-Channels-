from django.urls import path
from . import consumers

websocket_urlpatterns = [
    # WebSocket route that captures the room name from the URL
    path('ws/<str:room_name>/', consumers.ChatConsumer.as_asgi()),
]
