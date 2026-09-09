from orders.models import Dish, Category, Order, OrderItem
from django.contrib.auth.models import User
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    
    class Meta:
            model = User
            fields = "__all__"
            
class OrderSerializer(serializers.ModelSerializer):
    category = UserSerializer(read_only = True)
    
    class Meta:
        model = Order
        fields = ['id','name','category']