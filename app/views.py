from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view

from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from django.db.models import Q
# from simple_mail.mail import send_mail

from app.models import *
from .serializer import *
from .pagination import *
from rest_framework import generics
from rest_framework.pagination import PageNumberPagination
# Create your views here.

def send_mail(request):
    if request.method == 'POST':
        form_data = request.POST
        send_mail(
        'Form submission',
        f'You received a new submission with the following data:\n{form_data}',
        'sender@example.com',
        ['recipient@example.com'],
        )
    return form_data

def carsPage(request, model_slug=None):
    models = None
    cars = None
    if model_slug != None:
        models = get_object_or_404(Model, slug=model_slug)
        cars = Car.objects.filter(model=models, is_available=True)
        car_count = cars.count()
    else:
        cars = Car.objects.all().filter(is_available=True)
        car_count = cars.count()
    context = {
        'models':models,
        'cars':cars,
        'car_count':car_count,
    }
    return render(request, 'products.html', context)

class StandardResultsSetPagination(PageNumberPagination):
    page_size = 100
    page_size_query_param = 'page_size'
    max_page_size = 1000

@api_view(['GET',])
def api_cars(request):
    if request.method == "GET":
        cars = Car.objects.all()

        # Set up pagination
        paginator = PageNumberPagination()
        paginator.page_size = 300
        result_page = paginator.paginate_queryset(cars, request)

        # Serialize the result page
        serializer = CarSerializer(result_page, many=True)
        return Response(serializer.data)

@api_view(['GET',])
def api_models(request):
    if request.method == "GET":
        models = Model.objects.all()
        serializer = ModelSerializer(models, many=True)
        return Response(serializer.data)


@api_view(['GET'])
def getCarDetails(request, car_id):
    if request.method == "GET":
        car= Car.objects.filter(id = car_id)
        serializer = CarSerializer(car, many=True)
        return Response(serializer.data)


@api_view(['GET'])
def getCarsByModel(request, model_id):
    if request.method == "GET":
        model = get_object_or_404(Model, id=model_id)
        cars = Car.objects.filter(model=model)
        serializer = CarSerializer(cars, many=True)
        return Response(serializer.data)

@api_view(['GET'])
def get_blogs(request):
    if request.method == "GET":
        blogs = Blogs.objects.all()
        serializer = BlogsSerializer(blogs, many=True)
        return Response(serializer.data)

@api_view(['GET'])
def getBlogDetails(request, blog_id):
    if request.method == "GET":
        blogs= Blogs.objects.filter(id = blog_id)
        serializer = BlogsSerializer(blogs, many=True)
        return Response(serializer.data)