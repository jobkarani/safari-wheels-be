from django.db import models
from django.urls import reverse
from pyuploadcare.dj.models import ImageField
# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=100, unique=True)

    class Meta:
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def get_url(self):
        return reverse('products_by_category', args=[self.slug])

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True)
    image = ImageField( manual_crop="")
    image2 = ImageField(blank=True, null=True, manual_crop="")
    image3 = ImageField(blank=True,null=True, manual_crop="")
    description = models.TextField(max_length=4000)
    new_price = models.FloatField()
    old_price = models.FloatField()
    is_available = models.BooleanField(default = True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

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

class Service(models.Model):
    image = ImageField( manual_crop="")
    name = models.CharField(max_length=100, blank=False)
    paragrapagh1 = models.TextField(max_length=1000, blank=False, null=True)
    paragrapagh2 = models.TextField(max_length=1000, blank=True, null=True)
    paragrapagh3 = models.TextField(max_length=1000, blank=True, null=True)

    def __str__(self):
        return self.name
