from django.urls import path

from chat import consumers

websocket_urlpatterns = [
    path('ws/<int:room_id>/', consumers.ChatConsumer.as_asgi()),
]