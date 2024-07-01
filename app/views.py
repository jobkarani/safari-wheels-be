from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view, authentication_classes,permission_classes
from django.shortcuts import get_object_or_404, render

from app.models import *
from .serializer import *
from .pagination import *
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

def carsPage(request, brand_slug=None):
    brands = None
    cars = None
    if brand_slug != None:
        brands = get_object_or_404(Brand, slug=brand_slug)
        cars = Car.objects.filter(brand=brands, is_available=True)
        car_count = cars.count()
    else:
        cars = Car.objects.all().filter(is_available=True)
        car_count = cars.count()
    context = {
        'brands':brands,
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
def api_brands(request):
    if request.method == "GET":
        brands = Brand.objects.all()
        serializer = BrandSerializer(brands, many=True)
        return Response(serializer.data)


@api_view(['GET'])
def getCarDetails(request, car_id):
    if request.method == "GET":
        car= Car.objects.filter(id = car_id)
        serializer = CarSerializer(car, many=True)
        return Response(serializer.data)


@api_view(['GET'])
def getCarsByBrand(request, brand_id):
    if request.method == "GET":
        brand = get_object_or_404(Brand, id=brand_id)
        cars = Car.objects.filter(brand=brand)
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