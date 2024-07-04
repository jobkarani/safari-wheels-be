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
    class Meta:
        model = Car
        fields = ['id', 'name', 'image', 'description','location', 'phone_number', 'no_of_persons', 'transmission', 'price', 'is_available','category']