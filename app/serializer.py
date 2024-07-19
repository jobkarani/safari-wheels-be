from rest_framework import serializers
from .models import *
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = User
        fields = ['id', 'email', 'username', 'password']

class ProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    class Meta(object):
        model = Profile
        fields = ['user', 'full_names', 'email', 'phone_number', 'id_number', 'id_front_image', 'id_back_image', 'location']

class CarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Car
        fields = ['id', 'name', 'image', 'description','location', 'phone_number', 'no_of_persons', 'transmission', 'price', 'category']

class ReviewSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    car = serializers.PrimaryKeyRelatedField(queryset=Car.objects.all())
    class Meta:
        model = Review
        fields = ['id', 'user', 'car', 'rating', 'comment', 'created_at']