from django.contrib import admin

from app.models import *

# Register your models here.

class CarAdmin(admin.ModelAdmin):
    list_display = ('name', 'location', 'price','category')

admin.site.register(Car, CarAdmin )
admin.site.register(Profile)