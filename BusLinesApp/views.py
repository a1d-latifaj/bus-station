from mapbox import Directions
from .models import BusRoute, Station
from django.http import JsonResponse
from .models import BusRoute, RouteStop
from django.shortcuts import render


# def get_bus_route_and_locations(request, route_id):
#     try:
#         bus_route = BusRoute.objects.get(pk=route_id)
#         start_station = bus_route.start_station
#         end_station = bus_route.end_station
#         route_stops = RouteStop.objects.filter(
#             route=bus_route).order_by('order')

#         stops_data = [{
#             "name": stop.station.name,
#             "latitude": stop.station.latitude,
#             "longitude": stop.station.longitude,
#             "order": stop.order
#         } for stop in route_stops]

#         # JSON
#         response_data = {
#             "busRoute": {
#                 "startStation": {
#                     "name": start_station.name,
#                     "latitude": start_station.latitude,
#                     "longitude": start_station.longitude
#                 },
#                 "stops": stops_data,
#                 "endStation": {
#                     "name": end_station.name,
#                     "latitude": end_station.latitude,
#                     "longitude": end_station.longitude
#                 }
#             }
#         }

#         return JsonResponse(response_data)

#     except BusRoute.DoesNotExist:
#         return JsonResponse({'error': 'Bus route not found'}, status=404)


import requests
from django.http import JsonResponse

def get_bus_route_and_locations(request, route_id):
    try:
        bus_route = BusRoute.objects.get(pk=route_id)
        start_station = bus_route.start_station
        end_station = bus_route.end_station
        route_stops = RouteStop.objects.filter(
            route=bus_route).order_by('order')

        stops_data = [{
            "name": stop.station.name,
            "latitude": stop.station.latitude,
            "longitude": stop.station.longitude,
            "order": stop.order
        } for stop in route_stops]

        # Calculate driving distance from start to end station
        driving_distance_start_to_end = calculate_direct_driving_distance(start_station, end_station)

        # Calculate driving distances between stops
        stop_distances = {}
        last_stop = start_station
        total_distance = 0
        for stop in route_stops:
            distance = calculate_direct_driving_distance(last_stop, stop.station)
            stop_distances[stop.order] = distance
            total_distance += distance
            last_stop = stop.station
        # Add distance from last stop to end station
        stop_distances[len(route_stops) + 1] = calculate_direct_driving_distance(last_stop, end_station)
        total_distance += stop_distances[len(route_stops) + 1]

        # JSON
        response_data = {
            "busRoute": {
                "startStation": {
                    "name": start_station.name,
                    "latitude": start_station.latitude,
                    "longitude": start_station.longitude
                },
                "stops": stops_data,
                "endStation": {
                    "name": end_station.name,
                    "latitude": end_station.latitude,
                    "longitude": end_station.longitude
                },
                "drivingDistanceStartToEnd": driving_distance_start_to_end,
                "stopDistances": stop_distances,
                "totalDistance": total_distance
            }
        }

        return JsonResponse(response_data)

    except BusRoute.DoesNotExist:
        return JsonResponse({'error': 'Bus route not found'}, status=404)

def calculate_direct_driving_distance(start_station, end_station):
    access_token = 'pk.eyJ1IjoiYWlkbGF0aWZhajk0IiwiYSI6ImNsdmlscXpndzFndjUyaXBlYzhqZHRiYXQifQ.8QsQMPqAZUFXGI4jh1Dmsg'
    start_coordinates = f"{start_station.longitude},{start_station.latitude}"
    end_coordinates = f"{end_station.longitude},{end_station.latitude}"
    
    url = f"https://api.mapbox.com/directions/v5/mapbox/driving/{start_coordinates};{end_coordinates}?steps=true&access_token={access_token}"
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        driving_distance_meters = data['routes'][0]['distance']
        driving_distance_km = driving_distance_meters / 1000
        return driving_distance_km
    else:
        return None


def display_map(request, route_id):
    return render(request, 'real_time_bus_tracking.html', {'route_id': route_id})


def get_all_bus_routes_and_locations(request):
    try:
        bus_routes = BusRoute.objects.all()
        all_routes_data = []
        for idx, bus_route in enumerate(bus_routes, start=1):
            start_station = bus_route.start_station
            end_station = bus_route.end_station
            route_stops = RouteStop.objects.filter(
                route=bus_route).order_by('order')

            stops_data = [{
                "name": stop.station.name,
                "latitude": stop.station.latitude,
                "longitude": stop.station.longitude,
                "order": stop.order
            } for stop in route_stops]

            route_data = {
                "id": idx,  # Përdorim indeksin e for loop
                "startStation": {
                    "name": start_station.name,
                    "latitude": start_station.latitude,
                    "longitude": start_station.longitude
                },
                "stops": stops_data,
                "endStation": {
                    "name": end_station.name,
                    "latitude": end_station.latitude,
                    "longitude": end_station.longitude
                }
            }
            all_routes_data.append(route_data)

        # JSON
        response_data = {
            "busRoutes": all_routes_data
        }

        return JsonResponse(response_data)

    except BusRoute.DoesNotExist:
        return JsonResponse({'error': 'Bus routes not found'}, status=404)


def display_all_maps(request):
    return render(request, 'real_time_all.html')

from django.http import JsonResponse
from asgiref.sync import sync_to_async
from datetime import datetime, timedelta
from .models import BusRoute, Station, RouteStop

@sync_to_async
def get_bus_route(route_id):
    return BusRoute.objects.get(pk=route_id)

@sync_to_async
def get_station_by_id(station_id):
    return Station.objects.get(pk=station_id)

@sync_to_async
def get_route_stops(route_id):
    return list(RouteStop.objects.filter(route_id=route_id).order_by('order'))

async def route_detail_view(request, route_id):
    try:
        bus_route = await get_bus_route(route_id)
        
        start_station = await get_station_by_id(bus_route.start_station_id)
        end_station = await get_station_by_id(bus_route.end_station_id)
        
        route_stops = await get_route_stops(route_id)
        stops_data = []
        total_distance = 0.0
        last_stop = start_station
        departure_time = bus_route.start_time
        
        for i, stop in enumerate(route_stops):
            station = await get_station_by_id(stop.station_id)
            distance_to_stop = calculate_direct_driving_distance(last_stop, station)
            
            # Calculate distance to the next stop
            if i < len(route_stops) - 1:
                next_station = await get_station_by_id(route_stops[i + 1].station_id)
                distance_to_next = calculate_direct_driving_distance(station, next_station)
            else:
                distance_to_next = None
            
            stops_data.append({
                "name": station.name,
                "latitude": station.latitude,
                "longitude": station.longitude,
                "order": stop.order,
                "distanceToPrevious": distance_to_stop,
                "distanceToNext": distance_to_next,  # Add distance to the next stop
                "arrivalTime": (departure_time + timedelta(hours=stop.arrival_time.hour, minutes=stop.arrival_time.minute)).strftime("%Y-%m-%d %H:%M:%S")
            })
            total_distance += distance_to_stop
            last_stop = station
            departure_time += timedelta(hours=stop.arrival_time.hour, minutes=stop.arrival_time.minute)
        
        distance_to_end = calculate_direct_driving_distance(last_stop, end_station)
        total_distance += distance_to_end
        
        distance_to_first_stop = calculate_direct_driving_distance(start_station, await get_station_by_id(route_stops[0].station_id))
        total_distance += distance_to_first_stop
        
        response_data = {
            "busRoute": {
                "startStation": {
                    "name": start_station.name,
                    "latitude": start_station.latitude,
                    "longitude": start_station.longitude,
                    "departureTime": bus_route.start_time.strftime("%Y-%m-%d %H:%M:%S")
                },
                "stops": stops_data,
                "endStation": {
                    "name": end_station.name,
                    "latitude": end_station.latitude,
                    "longitude": end_station.longitude,
                    "distanceToPrevious": distance_to_end,
                    "arrivalTime": bus_route.end_time.strftime("%Y-%m-%d %H:%M:%S") if bus_route.end_time else None
                },
                "totalDistance": total_distance
            }
        }

        return JsonResponse(response_data)

    except BusRoute.DoesNotExist:
        return JsonResponse({'error': 'Bus route not found'}, status=404)


from django.conf import settings
from django.shortcuts import render

def index(request):
    mapbox_access_token = settings.MAPBOX_ACCESS_TOKEN
    return render(request, 'index.html', {'mapbox_access_token': mapbox_access_token})



    #ADD ROUTE
from django.http import JsonResponse
from django.shortcuts import render
from django.views.generic import TemplateView
from .models import Bus, BusRoute, Station, RouteStop
from datetime import datetime
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.db.models import Max

class AddRouteView(TemplateView):
    template_name = 'add_route.html'

    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['buses'] = Bus.objects.all()
        context['stations'] = Station.objects.all()
        return context

    def post(self, request, *args, **kwargs):
        try:
            # Parse data from the request body
            data = request.POST
            bus_id = data.get('bus_id')
            start_station_id = data.get('start_station_id')
            end_station_id = data.get('end_station_id')
            start_time_str = data.get('start_time')
            end_time_str = data.get('end_time', None)  # Optional
            stops_data = zip(data.getlist('station[]'), data.getlist('arrival_time[]'))

            # Validate data
            if not all([bus_id, start_station_id, end_station_id, start_time_str]):
                return JsonResponse({'error': 'Missing required data'}, status=400)

            # Convert time strings to datetime objects
            start_time = datetime.strptime(start_time_str, '%Y-%m-%dT%H:%M')
            end_time = datetime.strptime(end_time_str, '%Y-%m-%dT%H:%M') if end_time_str else None

            # Retrieve related objects
            bus = Bus.objects.get(pk=bus_id)
            start_station = Station.objects.get(pk=start_station_id)
            end_station = Station.objects.get(pk=end_station_id)

            # Create the bus route
            route = BusRoute.objects.create(
                bus=bus,
                start_station=start_station,
                end_station=end_station,
                start_time=start_time,
                end_time=end_time
            )

            # Create stops
            max_order = RouteStop.objects.filter(route=route).aggregate(Max('order'))['order__max'] or 0
            for i, (station_id, arrival_time_str) in enumerate(stops_data, start=max_order + 1):
                station = Station.objects.get(pk=station_id)
                arrival_time = datetime.strptime(arrival_time_str, '%Y-%m-%dT%H:%M')
                RouteStop.objects.create(route=route, station=station, arrival_time=arrival_time, order=i)

            # Return success response
            return JsonResponse({'success': True, 'route_id': route.pk}, status=201)

        except (Bus.DoesNotExist, Station.DoesNotExist) as e:
            return JsonResponse({'error': 'Invalid bus or station ID'}, status=400)

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
