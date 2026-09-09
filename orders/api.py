from rest_framework.viewsets import GenericViewSet

from rest_framework import mixins

from orders.models import Dish
from orders.serializers import DishSerializer

class OrdersViewset(
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    GenericViewSet
    ):
    queryset = Dish.objects.all()
    serializer_class = DishSerializer