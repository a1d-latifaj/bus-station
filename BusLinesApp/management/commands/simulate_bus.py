# management/commands/simulate_bus.py

import time
from django.core.management.base import BaseCommand
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from myapp.models import Route

class Command(BaseCommand):
    def handle(self, *args, **options):
        routes = Route.objects.all()
        channel_layer = get_channel_layer()

        for route in routes:
            waypoints = route.waypoints
            # Simulate bus movement
            for i in range(len(waypoints) - 1):
                start_point = waypoints[i]
                end_point = waypoints[i + 1]
                # Calculate intermediate positions between start and end points
                intermediate_positions = calculate_intermediate_positions(start_point, end_point, speed, time_interval)
                for position in intermediate_positions:
                    # Send position update to WebSocket clients
                    async_to_sync(channel_layer.group_send)(
                        'bus_updates',
                        {
                            'type': 'bus.update',
                            'position': position,
                        }
                    )
                    time.sleep(time_interval)
