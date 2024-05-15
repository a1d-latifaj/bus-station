from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import UserProfile, Address
from .models import Users  # Import the Users model

class UserRegisterForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    email = forms.EmailField()

    class Meta:
        model = Users
        fields = ['first_name', 'last_name', 'email', 'password1', 'password2']

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['profile_picture']

class UserAddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = ['street_address_1', 'street_address_2', 'town', 'city', 'country']
