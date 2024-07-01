from django.urls import path, re_path
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from app import views
from .views import *

schema_view = get_schema_view(
   openapi.Info(
      title="Onboarding Platform API",
      default_version='v1',
      description="Test description",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@snippets.local"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
   authentication_classes=[]
)

urlpatterns = [
    re_path('login', views.login),
    re_path('signup', views.signup),
    re_path('test_token', views.test_token),
    re_path('saveProfile', views.saveProfile),
    path('', views.carsPage, name='carsPage'),
    path('emails/', views.send_mail, name='email'),
    path('get_blogs/', views.get_blogs, name='blogs'),
    path('api_cars/', views.api_cars, name='apiCars' ),
    path('api_brands/', views.api_brands, name='apiBrands' ),
    path('getCarDetails/<int:car_id>/', views.getCarDetails, name='getCarDetails' ),
    path('api_brandcars/<int:brand_id>/', views.getCarsByBrand, name='apiBrandcars' ),
    path('getBlogDetails/<int:blog_id>/', views.getBlogDetails, name='Blog Details' ),
]
