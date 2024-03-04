from django.db import models

class Location(models.Model):
    name = models.CharField(max_length=100)
    location_type = models.CharField(max_length=100, choices=[('city', 'City'), ('village', 'Village'), ('hamlet', 'Hamlet')])

    def __str__(self):
        return f"{self.name} ({self.get_location_type_display()})"

class BusCompany(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=255)
    contact_info = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Bus(models.Model):
    company = models.ForeignKey(BusCompany, related_name='buses', on_delete=models.CASCADE)
    registration_number = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    seat_capacity = models.IntegerField()

    def __str__(self):
        return f"{self.model} - {self.registration_number}"

class Station(models.Model):
    name = models.CharField(max_length=255)
    latitude = models.FloatField()
    longitude = models.FloatField()
    location = models.ForeignKey(Location, on_delete=models.CASCADE, related_name='stations')   

    def __str__(self):
        return self.name


    
from django.db import models
# from .utils import calculate_driving_distance
from django.db import models
from django.db.models import F
from mapbox import Directions
import requests

class BusRoute(models.Model):
    bus = models.ForeignKey(Bus, related_name='routes', on_delete=models.CASCADE)
    start_station = models.ForeignKey(Station, related_name='start_routes', on_delete=models.CASCADE)
    end_station = models.ForeignKey(Station, related_name='end_routes', on_delete=models.CASCADE)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Route from {self.start_station.name} to {self.end_station.name}"




class RouteStop(models.Model):
    route = models.ForeignKey(BusRoute, related_name='stops', on_delete=models.CASCADE)
    station = models.ForeignKey(Station, related_name='route_stops', on_delete=models.CASCADE)
    arrival_time = models.DateTimeField()
    order = models.IntegerField(help_text="Order of the stop in the route")

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.order}. Stop at {self.station.name} for route {self.route}"



    # def calculate_driving_distance(self, destination):
    #     origin = (self.station.longitude, self.station.latitude)
    #     destination = (destination.longitude, destination.latitude)
    #     return calculate_driving_distance(origin, destination)



class RouteWaypoint(models.Model):
    route = models.ForeignKey(BusRoute, related_name='waypoints', on_delete=models.CASCADE)
    station = models.ForeignKey(Station, related_name='route_waypoints', on_delete=models.CASCADE)
    sequence = models.IntegerField(help_text="Order of the waypoint in the route")

    class Meta:
        ordering = ['sequence']

    def __str__(self):
        return f"Waypoint {self.sequence} at {self.station.name} for route {self.route}"
