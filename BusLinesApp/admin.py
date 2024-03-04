from django.contrib import admin
from .models import Location, BusCompany, Bus, Station, BusRoute, RouteStop, RouteWaypoint

@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ('name', 'location_type')

@admin.register(BusCompany)
class BusCompanyAdmin(admin.ModelAdmin):
    list_display = ('name', 'address', 'contact_info')

@admin.register(Bus)
class BusAdmin(admin.ModelAdmin):
    list_display = ('model', 'registration_number', 'company', 'seat_capacity')
    list_filter = ('company',)
    search_fields = ('model', 'registration_number')

@admin.register(Station)
class StationAdmin(admin.ModelAdmin):
    list_display = ('name', 'latitude', 'longitude', 'location')
    list_filter = ('location',)
    search_fields = ('name',)

@admin.register(BusRoute)
class BusRouteAdmin(admin.ModelAdmin):
    list_display = ('bus', 'start_station', 'end_station', 'start_time', 'end_time')
    list_filter = ('bus', 'start_station', 'end_station')

@admin.register(RouteStop)
class RouteStopAdmin(admin.ModelAdmin):
    list_display = ('route', 'station', 'arrival_time', 'order')
    list_filter = ('route', 'station')
    ordering = ('route', 'order')

    def get_ordering(self, request):
        return ['route', 'order']

@admin.register(RouteWaypoint)
class RouteWaypointAdmin(admin.ModelAdmin):
    list_display = ('route', 'station', 'sequence')
    list_filter = ('route', 'station')
    ordering = ('route', 'sequence')

