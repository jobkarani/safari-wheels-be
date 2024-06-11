from django.urls import path
from app import views

urlpatterns = [
    path('', views.carsPage, name='carsPage'),
    path('emails/', views.send_mail, name='email'),
    path('get_blogs/', views.get_blogs, name='blogs'),
    path('api_cars/', views.api_cars, name='apiCars' ),
    path('api_models/', views.api_models, name='apiModels' ),
    path('getCarDetails/<int:car_id>/', views.getCarDetails, name='getCarDetails' ),
    path('api_modelcars/<int:model_id>/', views.getCarsByModel, name='apiModelcars' ),
    path('getBlogDetails/<int:blog_id>/', views.getBlogDetails, name='Blog Details' ),
]
