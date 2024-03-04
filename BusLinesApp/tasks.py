from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from .models import BusPosition
from django.utils import timezone

@shared_task
def broadcast_bus_positions():
    """
    Task to broadcast bus positions to WebSocket consumers.
    """
    channel_layer = get_channel_layer()
    bus_positions = BusPosition.objects.all()
    for position in bus_positions:
        async_to_sync(channel_layer.group_send)(
            "bus_positions_group",
            {
                "type": "bus_position_update",
                "message": {
                    "latitude": position.latitude,
                    "longitude": position.longitude,
                    "timestamp": position.timestamp.isoformat()
                }
            }
        )
