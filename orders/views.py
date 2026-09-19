from django.shortcuts import render
from django.http import HttpResponse

from orders.models import Dish, Category, Order, OrderItem
from django.views import View
from django.views.generic import TemplateView
# Create your views here.


class ShowOrdersView(TemplateView):
   template_name = "orders/show_orders.html"

         
   def get_context_data(self, **kwargs) -> dict[str, Any]:
       context = super().get_context_data(**kwargs)
       context["orders"] = Order.objects.all()
       return context
   
   
class ShowDishsView(TemplateView):
   template_name = "orders/show_dishs.html"

         
   def get_context_data(self, **kwargs) -> dict[str, Any]:
       context = super().get_context_data(**kwargs)
       context["dishs"] = Dish.objects.all()
       return context   