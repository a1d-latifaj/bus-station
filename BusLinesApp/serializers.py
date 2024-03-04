from rest_framework import serializers
from .models import BusCompany, Bus, BusPosition, BusRoute, RouteStop

class BusCompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = BusCompany
        fields = '__all__'

class BusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bus
        fields = '__all__'

class BusPositionSerializer(serializers.ModelSerializer):
    class Meta:
        model = BusPosition
        fields = '__all__'

class BusRouteSerializer(serializers.ModelSerializer):
    buses = BusSerializer(many=True, read_only=True)

    class Meta:
        model = BusRoute
        fields = '__all__'

class RouteStopSerializer(serializers.ModelSerializer):
    class Meta:
        model = RouteStop
        fields = '__all__'
