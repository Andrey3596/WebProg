from orders.models import Dish, Category

from rest_framework import serializers


class CategorySerializer(serializers.ModelSerializer):
    
    class Meta:
            model = Category
            fields = "__all__"
            
class DishSerializer(serializers.ModelSerializer):
    group = CategorySerializer(read_only = True)
    
    class Meta:
        model = Dish
        fields = ['id','name','category']