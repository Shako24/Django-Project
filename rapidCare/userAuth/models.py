from django.db import models
from django.contrib.auth.models import AbstractUser
from phonenumber_field.modelfields import PhoneNumberField

# Create your models here.


class CustomUser(AbstractUser):
    phone_number = PhoneNumberField(null=True, blank=True, unique=False)
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['phone_number', 'email', 'password']

    def __str__(self):
        return str(f'{self.username}')


class Profile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    img = models.ImageField(default='default.jpg', upload_to='profile_pics')

    def __str__(self):
        return f'{self.user.username} Profile'


class Address(models.Model):
    user = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, null=True, blank=True)
    state = models.CharField(max_length=15)
    area = models.CharField(max_length=30)
    unitNo = models.CharField(max_length=10)
    buildingName = models.CharField(max_length=20, null=True, blank=True)
    nearestLandmark = models.CharField(max_length=30, null=True, blank=True)
    mapLatLng = models.CharField(max_length=50, default='None')
    googleMapsLink = models.CharField(max_length=100, default='None')
    deviceID = models.CharField(max_length=36, null=True, blank=True, unique=True)

    def __str__(self):
        address = f'{self.unitNo}, {self.area}, {self.state}'

        return address
