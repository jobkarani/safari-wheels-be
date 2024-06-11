from django.contrib import admin

from app.models import *

# Register your models here.

class Modeladmin(admin.ModelAdmin):
    list_display = ('name','slug')
    prepopulated_fields = {'slug': ('name',)}

class CarAdmin(admin.ModelAdmin):
    list_display = ('name', 'location', 'price','model', 'is_available')
    prepopulated_fields = {'slug': ('name',)}

admin.site.register(Car, CarAdmin )
admin.site.register(Model, Modeladmin)
admin.site.register(Blogs)