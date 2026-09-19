from orders.models import Dish, Category, Order, OrderItem
from django.contrib.auth.models import User
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer): 
    class Meta:
            model = User
            fields = ['id', 'username']
      
      
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']   
        
class DishSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)  
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(),
        write_only=True,
        source='category'
    )  
    class Meta:
        model = Dish
        fields = ['id', 'name', 'description', 'price', 'category', 'category_id']  
         
class OrderItemSerializer(serializers.ModelSerializer):
    dish = DishSerializer(read_only=True)
    dish_id = serializers.PrimaryKeyRelatedField(
        queryset=Dish.objects.all(),
        write_only=True,
        source='dish'
    )
    class Meta:
        model = OrderItem
        fields = ['id', 'order', 'dish', 'dish_id', 'quantity', 'price']
     

class OrderSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    user_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), write_only=True, source='user'
    )
    items = OrderItemSerializer(many=True,read_only=True)
    class Meta:
        model = Order
        fields = ['id', 'user', 'user_id', 'created_at', 'status', 'total_amount', 'items']
        

