from django.contrib import admin

from app.models import *

# Register your models here.

class CarAdmin(admin.ModelAdmin):
    list_display = ('name', 'location', 'price','category')

class ProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'full_names', 'user', 'phone_number', 'location')
    
admin.site.register(Car, CarAdmin )
admin.site.register(Profile, ProfileAdmin)
admin.site.register(Review)