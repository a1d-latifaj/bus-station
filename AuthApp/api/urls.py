from django.urls import path
from . import views

urlpatterns = [
    path('countries/', views.fetch_countries, name='fetch_countries'),
    path('register/', views.RegisterAPIView.as_view(), name='register_user'),
    path('verify-email/', views.VerifyEmailAPIView.as_view(), name='verify_email'),
    path('user/profile/', views.UserProfileAPIView.as_view(), name='user_profile'),
    path('user/address/', views.UserAddressAPIView.as_view(), name='user_address'),
]
