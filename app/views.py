from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, authentication_classes,permission_classes
from django.shortcuts import get_object_or_404

from app.models import *
from .serializer import *
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from dj_rest_auth.registration.views import SocialLoginView

class GoogleLogin(SocialLoginView): # if you want to use Authorization Code Grant, use this
    adapter_class = GoogleOAuth2Adapter
    callback_url = "https://www.safariwheels.co.ke/"
    client_class = OAuth2Client
    
@api_view(['POST'])
def login(request):
    user = get_object_or_404(User, email=request.data['email'])
    if not user.check_password(request.data['password']):
        return Response({"detail": "Invalid credentials."}, status=status.HTTP_401_UNAUTHORIZED)
    
    refresh = RefreshToken.for_user(user)
    serializer = UserSerializer(instance=user)

    return Response({
        "refresh": str(refresh),
        "access": str(refresh.access_token),
        "user": serializer.data
    })

@api_view(['POST'])
def signup(request):
    # Check if username already exists
    username = request.data.get('username')
    if User.objects.filter(username=username).exists():
        return Response({"error": "Username already exists."}, status=status.HTTP_400_BAD_REQUEST)

    # Continue with the regular signup process if username is not taken
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        user = User.objects.get(username=request.data['username'])
        user.set_password(request.data['password'])
        user.save()

        refresh = RefreshToken.for_user(user)

        return Response({
            "refresh": str(refresh),
            "access": str(refresh.access_token),
            "user": serializer.data
        })
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def check_username_exists(request):
    username = request.query_params.get('username', None)
    if username is None:
        return Response({"error": "Username parameter is required."}, status=status.HTTP_400_BAD_REQUEST)

    exists = User.objects.filter(username=username).exists()
    if exists:
        return Response({"username_exists": True}, status=status.HTTP_200_OK)
    else:
        return Response({"username_exists": False}, status=status.HTTP_200_OK)

@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def test_token(request):
    return Response(f"passed for {request.user.email}")

@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def saveProfile(request):
    user = request.user
    try:
        profile = Profile.objects.get(user=user)
        serializer = ProfileSerializer(profile, data=request.data, partial=True)
    except Profile.DoesNotExist:
        serializer = ProfileSerializer(data=request.data)

    if serializer.is_valid():
        # Remove the user from validated_data if it's in request.data
        serializer.save(user=user)
        return Response({"profile": serializer.data})
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def profile_check(request):
    user = request.user

    try:
        profile = Profile.objects.get(user=user)
        return Response({"hasProfile": True}, status=status.HTTP_200_OK)
    except Profile.DoesNotExist:
        return Response({"hasProfile": False}, status=status.HTTP_200_OK)
    
@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def profile_detail(request, id):
    try:
        profile = Profile.objects.get(pk=id)
    except Profile.DoesNotExist:
        return Response({"error": "Profile not found"}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = ProfileSerializer(profile)
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
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def post_car(request):
    profile = request.user.profile 
    if profile.user_type != 'Owner':
        return Response({"error": "Only car owners can post cars."}, status=status.HTTP_403_FORBIDDEN)

    serializer = CarSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(owner=profile)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def list_categories(request):
    categories = {key: value for key, value in CATEGORY_CHOICES}
    return Response(categories)

@api_view(['POST'])
def create_review(request):
    if request.method == 'POST':
        serializer = ReviewSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def list_reviews(request, car_id):
    car = get_object_or_404(Car, id=car_id)
    reviews = car.reviews.all()
    serializer = ReviewSerializer(reviews, many=True)
    return Response(serializer.data)


@api_view(['GET', 'PUT', 'DELETE'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def review_detail(request, id):
    review = get_object_or_404(Review, id=id)

    if request.method == 'GET':
        serializer = ReviewSerializer(review)
        return Response(serializer.data)
    
    elif request.method == 'PUT':
        if review.user != request.user:
            return Response({'error': 'You can only edit your own review.'}, status=status.HTTP_403_FORBIDDEN)
        serializer = ReviewSerializer(review, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'DELETE':
        if review.user != request.user:
            return Response({'error': 'You can only delete your own review.'}, status=status.HTTP_403_FORBIDDEN)
        review.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['GET'])
def search_cars(request):
    name = request.query_params.get('name', None)
    location = request.query_params.get('location', None)

    cars = Car.objects.all()

    if name:
        cars = cars.filter(name__icontains=name)
    
    if location:
        cars = cars.filter(location__icontains=location)

    serializer = CarSerializer(cars, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK) 