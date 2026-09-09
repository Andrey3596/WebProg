from django.contrib import admin
from orders.models import Dish, Category
# Register your models here.


@admin.register(Dish)
class DishAdmin(admin.ModelAdmin):
    
    list_display = ['id','name','group']
    
    
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    
    list_display = ['id','name']