from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import OrderViewSet, QuickOrderView, CartValidateView

router = DefaultRouter()
router.register(r'orders', OrderViewSet, basename='order')

urlpatterns = [
    path('orders/quick-order/', QuickOrderView.as_view(), name='quick-order'),
    path('cart/validate/', CartValidateView.as_view(), name='cart-validate'),
    path('', include(router.urls)),
]
