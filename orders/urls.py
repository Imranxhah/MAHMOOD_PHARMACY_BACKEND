from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import OrderViewSet, QuickOrderView, CartValidateView, DeliveryChargeView

router = DefaultRouter()
router.register(r'orders', OrderViewSet, basename='order')

urlpatterns = [
    path('orders/quick-order/', QuickOrderView.as_view(), name='quick-order'),
    path('delivery-charges/', DeliveryChargeView.as_view(), name='delivery-charges'),
    path('cart/validate/', CartValidateView.as_view(), name='cart-validate'),
    path('', include(router.urls)),
]
