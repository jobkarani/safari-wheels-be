from rest_framework import serializers
from .models import *
from django.contrib.auth.models import User

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['id', 'full_names', 'phone_number', 'location', 'user_type']

class UserSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer(read_only=True)  # Nesting ProfileSerializer
    
    class Meta:
        model = User
        fields = ['id', 'email', 'username', 'password', 'profile']
        extra_kwargs = {
            'password': {'write_only': True}  # Ensure password is write-only
        }
        
    def create(self, validated_data):
        user = User.objects.create(
            email=validated_data['email'],
            username=validated_data['username'],
        )
        user.set_password(validated_data['password'])
        user.save()
        Profile.objects.create(user=user)
        return user
    
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