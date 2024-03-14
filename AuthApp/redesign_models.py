from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.conf import settings
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.utils import timezone

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_admin', True)
        extra_fields.setdefault('is_passenger', False)
        extra_fields.setdefault('is_bus_company_management', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)

class Users(AbstractUser):
    email = models.EmailField(unique=True)
    is_passenger = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_bus_company_management = models.BooleanField(default=False)
    username = None  # Remove username field
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    objects = CustomUserManager()

    def __str__(self):
        return self.email

# UsersProfile: aidlatifaj, profile_pictures/aidlatifaj.jpg, +38349867737
class UsersProfile(models.Model):
    user = models.OneToOneField(Users, on_delete=models.CASCADE, related_name='profile')
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    address = models.OneToOneField('Addresses', on_delete=models.CASCADE, related_name='user_profile')
    gender = models.CharField(max_length=10, choices=[('male', 'Male'), ('female', 'Female'), ('other', 'Other')], blank=True, null=True)
    privacy = models.BooleanField(default=True)

    def __str__(self):
        return f"Profile of {self.user}"


# Method: SMS, E-Mail, Auth App
class BackupMethod(models.Model):
    title = models.CharField(max_length=50)

    def __str__(self):
        return self.title

# 2FA: aidlatifaj, True, 2 (E-Mail),
class _2FA(models.Model):
    user = models.OneToOneField(Users, on_delete=models.CASCADE, related_name='two_factor_settings')
    is_enabled = models.BooleanField(default=False)
    backup_method = models.ForeignKey(BackupMethod, on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return f"Two-Factor Authentication Settings for {self.user}"

# RecoveryCode: aidlatifaj, c47cecbf41f45672bbad8510f285868791ad6ca7f90185309298108ee0b98163
class RecoveryCode(models.Model):
    user_2fa = models.OneToOneField(_2FA, on_delete=models.CASCADE, related_name='recovery_code')
    code = models.CharField(max_length=255)

    def __str__(self):
        return f"Recovery Code for {_2FA.user}: {self.code}"

# Tokens: aidlatifaj, 6512-8542, 03/14/2024 17:00, 03/14/2024 17:05, True, 2FA
class Tokens(models.Model):
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    token = models.CharField(max_length=8)
    created_at = models.DateTimeField(default=timezone.now)    
    expire_at = models.DateTimeField(default=timezone.now)
    is_active = models.BooleanField(default=True)
    used_for = models.CharField(max_length=20, choices=[('reset_password', 'Reset Password'), ('verify_account', 'Verify Account'), ('2fa', '2FA'), ('other', 'Other')])



# For Addresses
class Countries(models.Model):
    country = models.CharField(max_length=30)
    svg_code = models.TextField()

class Cities(models.Model):
    city = models.CharField(max_length=30)
    country = models.ForeignKey(Countries, on_delete=models.CASCADE, related_name='cities')

class Addresses(models.Model):
    street_address_1 = models.CharField(max_length=50)
    street_address_2 = models.CharField(max_length=50)
    house_number = models.CharField(max_length=10, blank=True, null=True)
    zip_code = models.CharField(max_length=5)
    city = models.ForeignKey(Cities, on_delete=models.CASCADE, related_name='addresses')

class Coordinates(models.Model):
    address = models.OneToOneField(Addresses, on_delete=models.CASCADE, related_name='coordinates')
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)

# For Stations
class Stations(models.Model):
    station_name = models.CharField(max_length=50)
    address = models.OneToOneField(Addresses, on_delete=models.CASCADE, related_name='station')

# For Buses
class BusCompanies(models.Model):
    company = models.CharField(max_length=50)
    email = models.EmailField()
    phone_number = models.CharField(max_length=12)
    website = models.CharField(max_length=50)
    address = models.ForeignKey(Addresses, on_delete=models.CASCADE)

class Buses(models.Model):
    type_of_bus = models.CharField(max_length=50)
    company_id = models.ForeignKey(BusCompanies, on_delete=models.CASCADE)
    registration_number = models.CharField(max_length=11)
    seat_capacity = models.IntegerField()
    gps_device_id = models.CharField(max_length=20)


# For Bus Routes
class BusSchedules(models.Model):
    start_date = models.DateField()
    end_date = models.DateField()
    monday = models.BooleanField(default=False)
    tuesday = models.BooleanField(default=False)
    wednesday = models.BooleanField(default=False)
    thursday = models.BooleanField(default=False)
    friday = models.BooleanField(default=False)
    saturday = models.BooleanField(default=False)
    sunday = models.BooleanField(default=False)
    start_time = models.TimeField()
    end_time = models.TimeField()


class BusRoutes(models.Model):
    bus = models.ForeignKey(Buses, on_delete=models.CASCADE)
    start_station = models.ForeignKey(Stations, on_delete=models.CASCADE)
    end_station = models.ForeignKey(Stations, on_delete=models.CASCADE)
    schedule = models.ForeignKey(BusSchedules, on_delete=models.CASCADE)

class RouteStops(models.Model):
    route_id = models.ForeignKey(BusRoutes, on_delete=models.CASCADE)
    station_id = models.ForeignKey(Stations, on_delete=models.CASCADE)
    arrival_time = models.DateTimeField()
    order = models.IntegerField(help_text="Order of the stop in the route")
