from django.contrib import admin
from orders.models import Dish, Category, Order, OrderItem
# Register your models here.


@admin.register(Dish)
class DishAdmin(admin.ModelAdmin):
    list_display = ['id','name','price','category']
    
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id','name']
    
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'created_at', 'status', 'total_amount']
    
@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['id', 'order', 'dish', 'quantity', 'price']
    