from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from pyuploadcare.dj.models import ImageField
# Create your models here.

CATEGORY_CHOICES = (
    ('Private-hire', 'Private-hire'),
    ('Construction-hire', 'Construction-hire'),
    ('Transport-hire', 'Transport-hire'),
    ('Agricultural-hire', 'Agricultural-hire'),
    ('Airport Transfer', 'Airport Transfer')
)

TRANSMISSION_CHOICES = (
    ('Automatic', 'Automatic'),
    ('Manual', 'Manual'),
)

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    location = models.CharField(max_length=30)
    phoneNumber = models.CharField(max_length=10)

    def __str__(self):
        return "{} {} {} from {}".format(
            self.location, self.phoneNumber)    

class Car(models.Model):
    name = models.CharField(max_length=200, unique=True)
    image = ImageField( manual_crop="")
    description = models.TextField(max_length=4000)
    location = models.TextField(max_length=255, default='default_location')
    no_of_persons = models.IntegerField()
    transmission = models.CharField(
        max_length=60, choices=TRANSMISSION_CHOICES, default="Automatic")
    price = models.FloatField()
    phone_number = models.CharField(max_length=10)
    is_available = models.BooleanField(default = True)
    category = models.CharField(
        max_length=60, choices=CATEGORY_CHOICES, default="Private-hire")

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return self.name