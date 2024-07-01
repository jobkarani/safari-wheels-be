from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from pyuploadcare.dj.models import ImageField
# Create your models here.

CATEGORY_CHOICES = (
    ('Private-hire', 'Car Owner'),
    ('Construction-hire', 'Mechanic/Garage'),
    ('Transport-hire', 'Spare Parts Retailer'),
    ('Agricultural-hire', 'Spare Parts Retailer'),
)
MODEL_CHOICES = (
    ('Toyota', 'Toyota'),
    ('Nissan', 'Nissan'),
    ('Subaru', 'Subaru'),
    ('Mitsubishi', 'Mitsubishi'),
    ('Mercedes', 'Mercedes Benz'),
    ('BMW', 'BMW'),
    ('Audi', 'Audi'),
    ('Volkswagen', 'Volkswagen'),
    ('Honda', 'Honda'),
    ('Land Rover', 'Land Rover'),
    ('Ford', 'Ford'),
)

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    location = models.CharField(max_length=30)
    phoneNumber = models.CharField(max_length=10)

    def __str__(self):
        return "{} {} {} from {}".format(
            self.location, self.phoneNumber)    

class Brand(models.Model):
    name = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=100, unique=True)

    class Meta:
        verbose_name = 'brand'
        verbose_name_plural = 'brands'

    def get_url(self):
        return reverse('cars_by_brand', args=[self.slug])

    def __str__(self):
        return self.name

class Car(models.Model):
    name = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True)
    image = ImageField( manual_crop="")
    image2 = ImageField(blank=True, null=True, manual_crop="")
    image3 = ImageField(blank=True,null=True, manual_crop="")
    description = models.TextField(max_length=4000)
    location = models.TextField(max_length=255, default='default_location')
    no_of_persons = models.IntegerField()
    transmission = models.TextField(max_length=4000) # automatic or manual 
    price = models.FloatField()
    is_available = models.BooleanField(default = True)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return self.name

class Blogs(models.Model):
    image = ImageField( manual_crop="")
    heading = models.CharField(max_length=100, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    text = models.TextField(max_length=1000, blank=False, null=True)
    tex2 = models.TextField(max_length=1000, blank=True, null=True, default="")
    text3 = models.TextField(max_length=1000, blank=True, null=True, default="")

    def __str__(self):
        return self.heading
