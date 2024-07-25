from django.contrib.auth import get_user_model
from rest_framework import serializers
from .. models import UserProfile, Address, VerificationToken, Country, City


User = get_user_model()

class UserRegistrationSerializer(serializers.ModelSerializer):
    password1 = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'password1', 'password2')

    def validate(self, data):
        if 'password1' not in data or 'password2' not in data:
            raise serializers.ValidationError("Password and Verify Password are required.")
        if data['password1'] != data['password2']:
            raise serializers.ValidationError("Password fields didn't match.")
        return data

    def create(self, validated_data):
        user = User.objects.create_user(
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            email=validated_data['email'],
            password=validated_data['password1'],
        )
        return user


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['profile_picture'] 

    def update(self, instance, validated_data):
        instance.profile_picture = validated_data.get('profile_picture', instance.profile_picture)
        instance.save()
        return instance

class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = ['id', 'name']

class CitySerializer(serializers.ModelSerializer):
    country = CountrySerializer(read_only=True)

    class Meta:
        model = City
        fields = ['id', 'name', 'country']

class AddressSerializer(serializers.ModelSerializer):
    city = CitySerializer(read_only=True)
    country = CountrySerializer(read_only=True)
    city_id = serializers.IntegerField(write_only=True)
    country_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Address
        fields = ['street_address_1', 'street_address_2', 'town', 'city', 'country', 'city_id', 'country_id', 'latitude', 'longitude']
        extra_kwargs = {
            'latitude': {'required': False},
            'longitude': {'required': False},
        }

    def create(self, validated_data):
        city_id = validated_data.pop('city_id')
        country_id = validated_data.pop('country_id')
        address = Address.objects.create(**validated_data, city_id=city_id, country_id=country_id)
        return address

    def update(self, instance, validated_data):
        instance.street_address_1 = validated_data.get('street_address_1', instance.street_address_1)
        instance.street_address_2 = validated_data.get('street_address_2', instance.street_address_2)
        instance.town = validated_data.get('town', instance.town)
        instance.latitude = validated_data.get('latitude', instance.latitude)
        instance.longitude = validated_data.get('longitude', instance.longitude)
        
        if 'city_id' in validated_data:
            instance.city_id = validated_data['city_id']
        if 'country_id' in validated_data:
            instance.country_id = validated_data['country_id']

        instance.save()
        return instance

class VerifyEmailSerializer(serializers.Serializer):
    email = serializers.EmailField()
    token = serializers.CharField()

    def validate(self, data):
        try:
            user = User.objects.get(email=data['email'])
            verification_token = VerificationToken.objects.get(user=user, token=data['token'], is_active=True)
        except (User.DoesNotExist, VerificationToken.DoesNotExist):
            raise serializers.ValidationError("Invalid verification details.")
        return data

    def save(self, **kwargs):
        email = self.validated_data['email']
        user = User.objects.get(email=email)
        verification_token = VerificationToken.objects.get(user=user, token=self.validated_data['token'])
        verification_token.is_active = False
        verification_token.save()
        user.is_active = True
        user.save()
