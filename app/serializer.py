from rest_framework import serializers
from .models import *

class CarSerializer(serializers.ModelSerializer):
    model_name = serializers.CharField(source='model.name')
    model_slug = serializers.CharField(source='model.slug')
    model_id = serializers.IntegerField(source='model.id')
    class Meta:
        model = Car
        fields = ['id', 'name', 'slug', 'image', 'image2', 'image3', 'description','location', 'no_of_persons', 'transmission', 'price', 'is_available','model_name','model_slug','model_id']

class ModelSerializer(serializers.ModelSerializer):
    cars = CarSerializer(many=True, read_only=True)
    class Meta:
        model = Model
        fields = ['id', 'name', 'slug', 'cars']

class BlogsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Blogs
        fields = ['id', 'image', 'heading', 'created_at', 'text','tex2','text3']