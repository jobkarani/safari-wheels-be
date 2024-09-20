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
   path('auth/google/', GoogleLogin.as_view(), name='google_login'),
   re_path('login', views.login),
   re_path('signup', views.signup),
   re_path('test_token', views.test_token),
   path('check-username/', views.check_username_exists, name='check-username'),
   # path('profiles', ProfileListAPIView.as_view, name='profiles'),
   path('profile/save/', views.saveProfile, name='save_profile'),
   path('profile-check/', views.profile_check, name='profile-check'),
   path('profile/<int:id>/', views.profile_detail, name='profile_detail'),
   # path('profile/<int:id>/update/', views.update_profile, name='update_profile'),
   path('cars/', views.list_all_cars, name='list_all_cars'),
   path('cars/new/', views.post_car, name='post_car'),
   path('categories/', views.list_categories, name='list_categories'),
   path('getCarDetails/<int:car_id>/', views.car_details, name='getCarDetails' ),
   path('api_categorycars/<str:category>/', views.list_cars_by_category, name='apicategorycars' ),
   path('car/<int:car_id>/reviews/', list_reviews, name='list_reviews'),
   path('review/', create_review, name='create_review'),
   path('review/<int:id>/', review_detail, name='review_detail'),
   path('search/', search_cars, name='search-cars'),
]
