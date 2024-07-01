from rest_framework import serializers
from .models import *
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = User
        fields = ['id', 'email', 'username', 'password']

class ProfileSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = Profile
        fields = ['location','phoneNumber']

class CarSerializer(serializers.ModelSerializer):
    brand_name = serializers.CharField(source='brand.name')
    brand_slug = serializers.CharField(source='brand.slug')
    brand_id = serializers.IntegerField(source='brand.id')
    class Meta:
        model = Car
        fields = ['id', 'name', 'slug', 'image', 'image2', 'image3', 'description','location', 'no_of_persons', 'transmission', 'price', 'is_available','brand_name','brand_slug','brand_id']

class BrandSerializer(serializers.ModelSerializer):
    cars = CarSerializer(many=True, read_only=True)
    class Meta:
        model = Brand
        fields = ['id', 'name', 'slug', 'cars']

class BlogsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Blogs
        fields = ['id', 'image', 'heading', 'created_at', 'text','tex2','text3']