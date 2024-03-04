# # signals.py

# from django.db.models.signals import post_save
# from django.dispatch import receiver
# from channels.layers import get_channel_layer
# from asgiref.sync import async_to_sync
# from .models import BusPosition, RouteStop

# @receiver(post_save, sender=BusPosition)
# def broadcast_bus_position(sender, instance, **kwargs):
#     channel_layer = get_channel_layer()
#     async_to_sync(channel_layer.group_send)(
#         'bus_positions_group',
#         {
#             'type': 'bus_position_update',
#             'message': {
#                 'type': 'position',
#                 'latitude': instance.latitude,
#                 'longitude': instance.longitude,
#                 'timestamp': instance.timestamp.isoformat(),
#             }
#         }
#     )

# @receiver(post_save, sender=RouteStop)
# def broadcast_bus_stop(sender, instance, **kwargs):
#     channel_layer = get_channel_layer()
#     async_to_sync(channel_layer.group_send)(
#         'bus_positions_group',
#         {
#             'type': 'bus_stop_update',
#             'message': {
#                 'type': 'stop',
#                 'latitude': instance.latitude,
#                 'longitude': instance.longitude,
#                 'name': instance.name,
#             }
#         }
#     )
