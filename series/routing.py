from django.urls import path
from . import consumers

websocket_urlpatterns = [
    path('chat/<int:room_name>/', consumers.ChatConsumer),
]