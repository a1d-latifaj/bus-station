from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('AuthApp.urls')), 
    path('bus/',include('BusLinesApp.urls')),
    path('__debug__/', include('debug_toolbar.urls')),

    path('__reload__/', include('django_browser_reload.urls')),

]
