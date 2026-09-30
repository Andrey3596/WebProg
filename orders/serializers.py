from orders.models import Dish, Category, Order, OrderItem, Profile
from django.contrib.auth.models import User
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer): 
    class Meta:
            model = Profile
            fields = '__all__'
      
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__' 
        
class DishSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Dish
        fields = fields = '__all__' 
         
class OrderItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = OrderItem
        fields = '__all__'
     

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = fields = '__all__'
        

