from django.urls import path
from .views import DashboardStatsView, AdminAnalyticsView

urlpatterns = [
    path('analytics/dashboard/', DashboardStatsView.as_view(), name='dashboard-stats'),
    path('admin/dashboard-charts/', AdminAnalyticsView.as_view(), name='admin-charts'),
]
