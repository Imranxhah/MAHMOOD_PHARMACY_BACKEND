from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BannerViewSet, SendNotificationView

router = DefaultRouter()
router.register(r'banners', BannerViewSet, basename='banner')

urlpatterns = [
    path('marketing/notifications/send/', SendNotificationView.as_view(), name='send-notification'),
    path('', include(router.urls)),
]
