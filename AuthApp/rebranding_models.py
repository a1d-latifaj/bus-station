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

class UsersProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    gender = models.CharField(max_length=10, choices=[('male', 'Male'), ('female', 'Female'), ('other', 'Other')], blank=True, null=True)
    privacy = models.BooleanField(default=True)

    def __str__(self):
        return f"Profile of {self.user}"

class BackupMethod(models.Model):
    title = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class 2FA(models.Model):
    user = models.OneToOneField(Users, on_delete=models.CASCADE, related_name='two_factor_settings')
    is_enabled = models.BooleanField(default=False)
    backup_method = models.ForeignKey(BackupMethod, on_delete=models.SET_NULL, blank=True, null=True)
    recovery_codes = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"Two-Factor Authentication Settings for {self.user}"

    
class Tokens(models.Model):
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    token = models.CharField(max_length=8)
    created_at = models.DateTimeField(default=timezone.now)    
    expire_at = models.DateTimeField(default=timezone.now)
    is_active = models.BooleanField(default=True)