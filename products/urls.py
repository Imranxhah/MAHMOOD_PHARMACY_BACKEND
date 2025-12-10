from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    CategoryListView, 
    ProductViewSet, 
    ProductBulkUploadView, 
    FavoriteListView, 
    FavoriteToggleView
)

router = DefaultRouter()
router.register(r'products', ProductViewSet, basename='product')

urlpatterns = [
    path('', include(router.urls)),
    path('categories/', CategoryListView.as_view(), name='category-list'),
    path('products/bulk-upload/', ProductBulkUploadView.as_view(), name='bulk-upload'),
    path('favorites/', FavoriteListView.as_view(), name='favorite-list'),
    path('favorites/toggle/', FavoriteToggleView.as_view(), name='favorite-toggle'),
]
