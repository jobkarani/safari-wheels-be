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
    USER_TYPE_CHOICES = (
        ('Owner', 'Owner'),
        ('Renter', 'Renter'),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    full_names = models.CharField(max_length=100, null=True)
    phone_number = models.CharField(max_length=12, null=True)
    location = models.CharField(max_length=30, null=True)
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES, default='Renter')

    def __str__(self):
        return "{} - {} - {} - {}".format(self.user.username, self.full_names, self.user_type, self.location)  

class Car(models.Model):
    owner = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='cars', null=True)
    name = models.CharField(max_length=200)
    image = ImageField(manual_crop="")
    description = models.TextField(max_length=4000)
    location = models.TextField(max_length=255, default='Nairobi')
    no_of_persons = models.IntegerField()
    transmission = models.CharField(max_length=60, choices=TRANSMISSION_CHOICES, default="Automatic")
    price = models.FloatField()
    phone_number = models.CharField(max_length=12)
    category = models.CharField(max_length=60, choices=CATEGORY_CHOICES, default="Private-hire")

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return self.name
    
class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    car = models.ForeignKey(Car, on_delete=models.CASCADE, related_name='reviews')
    rating = models.IntegerField(default=1)  # Assuming rating out of 5
    comment = models.TextField(max_length=2000)

    class Meta:
        ordering = ['rating']

    def __str__(self):
        return f'{self.user.username} - {self.car.name} - {self.rating}'