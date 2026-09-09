from django.shortcuts import render
from django.http import HttpResponse

from orders.models import Dish
from django.views import View
from django.views.generic import TemplateView
# Create your views here.


class ShowOrdersView(TemplateView):
   template_name = "orders/show_students .html"

         
   def get_context_data(self, **kwargs) -> dict[str, Any]:
       context = super().get_context_data(**kwargs)
       context["dishes"] = Dish.objects.all
       return context