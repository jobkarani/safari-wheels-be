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
    print("Authenticated user:", user)
    if not request.user.is_authenticated:
        return Response({"detail": "User not authenticated."}, status=status.HTTP_401_UNAUTHORIZED)
    try:
        profile = Profile.objects.get(user=user)
        serializer = ProfileSerializer(profile, data=request.data)
    except Profile.DoesNotExist:
        serializer = ProfileSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save(user=user)
        return Response({"profile": serializer.data})
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def profile_check(request):
    user = request.user
    if not user.is_authenticated:
        return Response({"detail": "User not authenticated."}, status=status.HTTP_401_UNAUTHORIZED)
    
    try:
        profile = Profile.objects.get(user=user)
        return Response({"hasProfile": True}, status=status.HTTP_200_OK)
    except Profile.DoesNotExist:
        return Response({"hasProfile": False}, status=status.HTTP_200_OK)

# @api_view(['GET'])
# @authentication_classes([SessionAuthentication, TokenAuthentication])
# @permission_classes([IsAuthenticated])
# def profile_detail(request, id):
#     try:
#         profile = Profile.objects.get(pk=id)
#     except Profile.DoesNotExist:
#         return Response({"error": "Profile not found"}, status=status.HTTP_404_NOT_FOUND)

#     if request.method == 'GET':
#         serializer = ProfileSerializer(profile)
#         return Response(serializer.data)

# @api_view(['PUT'])
# @authentication_classes([SessionAuthentication, TokenAuthentication])
# @permission_classes([IsAuthenticated])
# def update_profile(request, id):
#     try:
#         profile = Profile.objects.get(pk=id)
#     except Profile.DoesNotExist:
#         return Response({"error": "Profile not found"}, status=status.HTTP_404_NOT_FOUND)

#     if request.method == 'PUT':
#         serializer = ProfileSerializer(profile, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# @authentication_classes([SessionAuthentication, TokenAuthentication])
# @permission_classes([IsAuthenticated])
# class ProfileListAPIView(APIView):
#     def post(self, request):
#         queryset = Profile.objects.all()

#         # Filter queryset based on query parameters
#         for key, value in request.data.items():
#             kwargs = {f'{key}__icontains': value}  # Case-insensitive partial match
#             queryset = queryset.filter(**kwargs)

#         serializer = ProfileSerializer(queryset, many=True)
#         return Response(serializer.data)


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

@api_view(['POST'])
def create_review(request):
    if request.method == 'POST':
        serializer = ReviewSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def list_reviews(request, car_id):
    car = get_object_or_404(Car, id=car_id)
    reviews = car.reviews.all()
    serializer = ReviewSerializer(reviews, many=True)
    return Response(serializer.data)

@api_view(['GET', 'PUT', 'DELETE'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
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