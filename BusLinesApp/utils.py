from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

async def send_bus_position_update(bus_position):
    channel_layer = get_channel_layer()
    await channel_layer.group_send(
        'bus_positions',
        {
            'type': 'broadcast_bus_position',
            'bus_position': bus_position
        }
    )


# utils.py
# import os
# from mapbox import Directions

# def calculate_driving_distance(origin, destination):
#     mapbox_token = os.getenv('pk.eyJ1IjoiYWlkbGF0aWZhaiIsImEiOiJjbHNoamd2ZTExajUzMmttaGIzNWcyYW5vIn0.mFt8U7wu4jJTf1r7HD5Edw')  # Make sure to set your Mapbox access token as an environment variable
#     service = Directions(access_token=mapbox_token)
#     response = service.directions([origin, destination], profile='mapbox/driving-traffic', steps=False)
    
#     if response.status_code == 200:
#         data = response.geojson()
#         if 'routes' in data:
#             route = data['routes'][0]
#             distance = route['distance']
#             distance_km = distance / 1000
#             return distance_km
#         else:
#             print("No routes found in the Mapbox Directions response.")
#             return None
#     else:
#         print(f"Error getting directions: {response.text}")
#         return None

import httpx
from django.conf import settings

async def calculate_driving_distance_async(start_coordinates, end_coordinates):
    access_token = settings.MAPBOX_ACCESS_TOKEN
    start_coordinates = f"{start_station.longitude},{start_station.latitude}"
    end_coordinates = f"{end_station.longitude},{end_station.latitude}"
    
    url = f"https://api.mapbox.com/directions/v5/mapbox/driving/{start_coordinates};{end_coordinates}"
    params = {
        "steps": "true",
        "access_token": access_token,
    }
    
    async with httpx.AsyncClient() as client:
        response = await client.get(url, params=params)
        
        if response.status_code == 200:
            data = response.json()
            driving_distance_meters = data['routes'][0]['distance']
            driving_distance_km = driving_distance_meters / 1000  # Convert meters to kilometers
            return driving_distance_km
        else:
            return None