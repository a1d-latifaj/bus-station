from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .forms import UserRegisterForm, UserProfileForm, UserAddressForm
from .models import Users, VerificationToken, Address, UserProfile
from .helpers import generate_verification_code, send_verification_email, verify_account
from django.contrib.auth.decorators import login_required



from django.contrib.auth import authenticate, login

def register_step1(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            registration_data = form.cleaned_data
            verification_code = generate_verification_code()
            user = Users.objects.create_user(
                email=registration_data['email'],
                password=registration_data['password1'],
                first_name=registration_data['first_name'],
                last_name=registration_data['last_name']
            )
            send_verification_email(registration_data['email'], verification_code)
            verification_token = VerificationToken.objects.create(
                user=user,
                token=verification_code
            )
            user = authenticate(request, username=registration_data['email'], password=registration_data['password1'])
            if user:
                login(request, user)
            request.session['registration_data'] = registration_data
            request.session['verification_token_id'] = verification_token.id
            return redirect('register_step2')
    else:
        form = UserRegisterForm()
    return render(request, 'register_step1.html', {'form': form})


@login_required
def register_step2(request):
    if request.method == 'POST':
        code = request.POST.get('verification_code')
        verification_token_id = request.session.get('verification_token_id')
        verification_token = VerificationToken.objects.get(id=verification_token_id)
        if code == verification_token.token:
            return redirect('register_step3')
        else:
            return redirect('verification_failed')
    return render(request, 'register_step2.html')


import os
import tempfile
from django.conf import settings
from django.core.files.base import ContentFile
import uuid


@login_required
def register_step3(request):
    user = request.user
    if request.method == 'POST':
        if hasattr(user, 'profile'):
            profile_form = UserProfileForm(request.POST, request.FILES, instance=user.profile)
        else:
            profile_form = UserProfileForm(request.POST, request.FILES)
        
        if profile_form.is_valid():
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()
            return redirect('register_step4')
    else:
        if hasattr(user, 'profile'):
            profile_form = UserProfileForm(instance=user.profile)
        else:
            profile_form = UserProfileForm()
    return render(request, 'register_step3.html', {'profile_form': profile_form})

@login_required
def register_step4(request):
    if request.method == 'POST':
        address_form = UserAddressForm(request.POST)
        if address_form.is_valid():
            address = address_form.save(commit=False)
            address.user = request.user  # Set the user for the address
            address.save()
            return redirect('register_complete')  # Adjust as needed
    else:
        address_form = UserAddressForm()
    return render(request, 'register_step4.html', {'address_form': address_form})


def register_complete(request):
    if request.method == 'GET':
        registration_data = request.session.get('registration_data')
        profile_data = request.session.get('profile_data')
        address_data = request.session.get('address_data')
        if registration_data and profile_data and address_data:
            user = Users.objects.create_user(
                email=registration_data['email'],
                password=registration_data['password1'],
                first_name=registration_data['first_name'],
                last_name=registration_data['last_name']
            )
            profile = UserProfile.objects.create(user=user, **profile_data)
            address = Address.objects.create(user=user, **address_data)
            user = authenticate(username=user.email, password=registration_data['password1'])
            if user:
                login(request, user)
                return redirect('dashboard')
    return render(request, 'register_complete.html')


def verify_account_view(request):
    if request.method == 'GET':
        email = request.GET.get('email')
        code = request.GET.get('code')
        user = Users.objects.get(email=email)
        if verify_account(user, code):
            return redirect('account_verified')
    return redirect('verification_failed')


def verification_failed(request):
    return render(request, 'verification_failed.html')  # Assuming you have a template named 'verification_failed.html'


# views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import UserRegistrationSerializer
from .models import Users, VerificationToken
from .helpers import generate_verification_code, send_verification_email
from rest_framework.parsers import JSONParser, FormParser
from rest_framework.decorators import parser_classes
from rest_framework.permissions import AllowAny 

class RegisterAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save(is_active=False)  
            verification_code = generate_verification_code()
            send_verification_email(user.email, verification_code)
            VerificationToken.objects.create(user=user, token=verification_code)
            return Response({"message": "User registered. Please verify your email."}, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




class VerifyEmailAPIView(APIView):
    permission_classes = [AllowAny]  

    def post(self, request):
        token = request.data.get('token')
        try:
            verification_token = VerificationToken.objects.get(token=token, is_active=True)
            user = verification_token.user
            user.is_active = True 
            user.save()

            verification_token.is_active = False
            verification_token.save()

            # Authenticate and login the user automatically
            # Note: authenticate() is not needed if you're not using it for additional checks
            login(request, user)  # Directly login the user without password check

            return Response({"message": "Email verified and logged in successfully."}, status=status.HTTP_200_OK)
        except VerificationToken.DoesNotExist:
            return Response({"error": "Invalid token"}, status=status.HTTP_400_BAD_REQUEST)


from .serializers import UserProfileSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.permissions import IsAuthenticated

from rest_framework.parsers import MultiPartParser, FormParser



class UserProfileAPIView(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def get(self, request, format=None):
        try:
            user_profile = request.user.profile
            serializer = UserProfileSerializer(user_profile)
            return Response(serializer.data)
        except UserProfile.DoesNotExist:
            return Response({'message': 'UserProfile does not exist.'}, status=status.HTTP_404_NOT_FOUND)

    def post(self, request, format=None):
        user_profile, created = UserProfile.objects.get_or_create(user=request.user)
        serializer = UserProfileSerializer(user_profile, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

from .serializers import AddressSerializer

class UserAddressAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = AddressSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=201)
        else:
            return Response(serializer.errors, status=400)



def register_view(request):
    return render(request, 'register.html')

def verify_email_view(request):
    return render(request, 'verify_email.html')

def profile_info_view(request):
    return render(request, 'profile_info.html')

def address_info_view(request):
    return render(request, 'address_info.html')


from django.http import JsonResponse
import requests

def fetch_countries(request):
    try:
        response = requests.get('https://restcountries.com/v3.1/all')
        response.raise_for_status()  # Raises an HTTPError if the response status code is 4XX/5XX
        countries = [{"name": country["name"]["common"], "code": country["cca2"]} for country in response.json()]
        return JsonResponse({"countries": countries})
    except requests.RequestException as e:
        return JsonResponse({"error": str(e)}, status=500)