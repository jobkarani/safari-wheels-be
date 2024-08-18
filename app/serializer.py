from rest_framework import serializers
from .models import *
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'username', 'password']

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['full_names', 'email', 'phone_number', 'id_number', 'id_front_image', 'id_back_image', 'location', 'user_type']

class CarSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.user.username')  # Show owner's username in serialized data

    class Meta:
        model = Car
        fields = ['id', 'name', 'image', 'description', 'location', 'phone_number', 'no_of_persons', 'transmission', 'price', 'category', 'owner']

class ReviewSerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField()

    class Meta:
        model = Review
        fields = ['id', 'user', 'car', 'rating', 'comment', 'username'] 

    def get_username(self, obj):
        return obj.user.username