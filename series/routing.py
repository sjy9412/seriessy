from django.urls import path
from . import consumers

websocket_urlpatterns = [
    path('series/<int:series_pk>/room/', consumers.ChatConsumer),
]