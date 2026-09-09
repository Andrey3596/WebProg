#from rest_framework.viewsets import GenericViewSet

from rest_framework import mixins, viewsets
from rest_framework.viewsets import ModelViewSet
from orders.models import Dish,Category, Order, OrderItem
from orders.serializers import OrderSerializer, CategorySerializer, DishSerializer, OrderItemSerializer

class OrdersViewSet(
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet
    ):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    
    
class CategorysViewSet(mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class DishsViewSet(mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet):
    queryset = Dish.objects.all()
    serializer_class = DishSerializer
    
class OrderItemsViewSet(mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet):
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer