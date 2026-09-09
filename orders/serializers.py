from orders.models import Dish, Category, Order, OrderItem
from django.contrib.auth.models import User
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer): 
    class Meta:
            model = User
            fields = "__all__"
      
      
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']   
        
class DishSerializer(serializers.ModelSerializer):
    category = CategorySerializer()  
    class Meta:
        model = Dish
        fields = ['id', 'name', 'description', 'price', 'category']  
         
class OrderItemSerializer(serializers.ModelSerializer):
    dish = DishSerializer()
    class Meta:
        model = OrderItem
        fields = ['id', 'order', 'dish', 'quantity', 'price']
     

class OrderSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    items = OrderItemSerializer(many=True)  # вложенные позиции
    class Meta:
        model = Order
        fields = ['id', 'user', 'created_at', 'status', 'total_amount', 'items']
        

