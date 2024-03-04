from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('register/step1/', views.register_step1, name='register_step1'),
    path('register/step2/', views.register_step2, name='register_step2'),
    path('register/step3/', views.register_step3, name='register_step3'),
    path('register/step4/', views.register_step4, name='register_step4'),
    path('register/complete/', views.register_complete, name='register_complete'),
    path('verification-failed/', views.verification_failed, name='verification_failed'),

    path('register/', views.register_view, name='register'),
    path('verify-email/', views.verify_email_view, name='verify_email'),
    path('profile-info/', views.profile_info_view, name='profile_info'),
    path('address-info/', views.address_info_view, name='address_info'),

    
    path('api/countries/', views.fetch_countries, name='fetch_countries'),

    path('api/register/', views.RegisterAPIView.as_view(), name='register_user'),
    path('api/verify-email/', views.VerifyEmailAPIView.as_view(), name='verify_email'),
    path('api/user/profile/', views.UserProfileAPIView.as_view(), name='user_profile'),
    path('api/user/address/', views.UserAddressAPIView.as_view(), name='user_address'),
   
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)