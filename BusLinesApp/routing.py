# busstation/routing.py
from django.urls import re_path
from .consumers import ArrivalTimeConsumer

websocket_urlpatterns = [
    re_path(r'ws/bus/arrival_times/$', ArrivalTimeConsumer.as_asgi()),
    # Add WebSocket URL pattern for http://localhost/bus/
    re_path(r'ws/bus/$', ArrivalTimeConsumer.as_asgi()),
]