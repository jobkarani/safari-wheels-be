from django.urls import path
from app import views

urlpatterns = [
    path('', views.productsPage, name='productsPage'),
    path('emails/', views.send_mail, name='email'),
    path('get_blogs/', views.get_blogs, name='blogs'),
    path('api_products/', views.api_products, name='apiProducts' ),
    path('api_categories/', views.api_categories, name='apiCategories' ),
    path('getProductDetails/<int:product_id>/', views.getProductDetails, name='getProductDetails' ),
    path('api_categoryproducts/<int:category_id>/', views.getProductsByCategory, name='apiCategoryproducts' ),
    path('getBlogDetails/<int:blog_id>/', views.getBlogDetails, name='Blog Details' ),
    path('get_services/', views.get_services, name='services'),
    path('getServiceDetails/<int:service_id>/', views.getServiceDetails, name='Service Details' ),
]
