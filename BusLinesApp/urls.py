from django.urls import path
from . import views

urlpatterns = [
    path('api/route_coordinates/<int:route_id>/',
         views.get_bus_route_and_locations, name='get_route_coordinates'),
    # Include other URLs as necessary
    path('map/<int:route_id>/', views.display_map, name='display_map'),
    path('api/all_routes_coordinates/', views.get_all_bus_routes_and_locations, name='all_routes_coordinates'),
    path('all_routes/', views.display_all_maps, name='display_all_maps'),
    # path('detail/<int:route_id>/', views.route_detail, name='route_detail'),
    path('route/<int:route_id>/', views.route_detail_view, name='route_detail'),
    path('', views.index, name='index'),


    path('add-route/', views.AddRouteView.as_view(), name='add_route'),

]
