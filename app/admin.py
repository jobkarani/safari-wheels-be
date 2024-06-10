from django.contrib import admin

from app.models import *

# Register your models here.

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name','slug')
    prepopulated_fields = {'slug': ('name',)}

class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'new_price', 'old_price','category', 'is_available')
    prepopulated_fields = {'slug': ('name',)}

admin.site.register(Product, ProductAdmin )
admin.site.register(Category, CategoryAdmin)
admin.site.register(Blogs)
admin.site.register(Service)