from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('AuthApp.urls')),  # Replace 'your_app' with the name of your Django app
    path('bus/',include('BusLinesApp.urls')),
    path('__debug__/', include('debug_toolbar.urls')),
]
