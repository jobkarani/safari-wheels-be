from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view, authentication_classes,permission_classes
from django.shortcuts import get_object_or_404, render

from app.models import *
from .serializer import *
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token
from rest_framework.pagination import PageNumberPagination
# Create your views here.


@api_view(['POST'])
def login(request):
    user = get_object_or_404(User, email = request.data['email'])
    if not user.check_password(request.data['password']):
        return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
    token , created = Token.objects.get_or_create(user=user)
    serializer = UserSerializer(instance=user)
    return Response({"token": token.key, "user": serializer.data})

@api_view(['POST'])
def signup(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        user = User.objects.get(username=request.data['username'])
        user.set_password(request.data['password'])
        user.save()
        token = Token.objects.create(user=user)
        return Response({"token": token.key, "user": serializer.data})
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def test_token(request):
    return Response("passed for {}".format(request.user.email))


@api_view(['POST'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def saveProfile(request):
    user = request.user
    try:
        # Try to get the existing Profile record for the authenticated user
        profile = Profile.objects.get(user=user)
        serializer = ProfileSerializer(profile, data=request.data)
    except Profile.DoesNotExist:
        # If no Profile record exists, create a new one
        serializer = ProfileSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save(user=user)  # Associate the user with the Profile record
        return Response({"profile": serializer.data})
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
class ProfileListAPIView(APIView):
    def post(self, request):
        queryset = Profile.objects.all()

        # Filter queryset based on query parameters
        for key, value in request.data.items():
            kwargs = {f'{key}__icontains': value}  # Case-insensitive partial match
            queryset = queryset.filter(**kwargs)

        serializer = ProfileSerializer(queryset, many=True)
        return Response(serializer.data)


@api_view(['GET'])
def list_all_cars(request):
    cars = Car.objects.all()
    serializer = CarSerializer(cars, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def list_cars_by_category(request, category):
    cars = Car.objects.filter(category=category)
    if cars.exists():
        serializer = CarSerializer(cars, many=True)
        return Response(serializer.data)
    else:
        return Response({"error": "No cars found in this category"}, status=status.HTTP_404_NOT_FOUND)
    
@api_view(['GET'])
def car_details(request, car_id):
    if request.method == "GET":
        car= Car.objects.filter(id = car_id)
        serializer = CarSerializer(car, many=True)
        return Response(serializer.data)
    else:
        return Response({"error": "Car not found"}, status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
def post_car(request):
    if request.method == 'POST':
        serializer = CarSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def list_categories(request):
    categories = {key: value for key, value in CATEGORY_CHOICES}
    return Response(categories)