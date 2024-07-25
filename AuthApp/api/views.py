from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from . serializers import UserRegistrationSerializer, UserProfileSerializer, AddressSerializer
from .. models import Users, VerificationToken
from .. helpers import generate_verification_code, send_verification_email
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