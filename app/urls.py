
from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from django.conf import settings
from orders.api import CategorysViewSet, DishsViewSet, OrdersViewSet, OrderItemsViewSet
from orders import views
from django.conf.urls.static import static


router = DefaultRouter()
router.register("orders",OrdersViewSet,basename="orders")
router.register('dishes', DishsViewSet, basename='dish')
router.register('orderitems', OrderItemsViewSet, basename='orderitem')
router.register('categories', CategorysViewSet, basename='category')


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.ShowOrdersView.as_view()),
    path('dishs/', views.ShowDishsView.as_view()),
    path('api/', include(router.urls)),
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
