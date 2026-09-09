from rest_framework.viewsets import GenericViewSet

from rest_framework import mixins

from orders.models import Dish,Category, Order, OrderItem
from orders.serializers import OrderSerializer

class OrdersViewset(
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    GenericViewSet
    ):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer