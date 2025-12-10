from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser
from rest_framework import status, renderers
from rest_framework.authentication import SessionAuthentication
from django.db.models import Sum, Count, F
from django.db.models.functions import TruncMonth, TruncDay
from django.utils.timezone import now
from datetime import timedelta
from orders.models import Order
from users.models import User
from products.models import Product
import json
from django.core.serializers.json import DjangoJSONEncoder

class DashboardStatsView(APIView):
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAdminUser]

    def get(self, request):
        total_sales = Order.objects.aggregate(total=Sum('total_amount'))['total'] or 0
        total_orders = Order.objects.count()
        total_users = User.objects.count()
        low_stock_products = Product.objects.filter(stock__lt=10).count()

        # Recent 5 Orders
        recent_orders = Order.objects.order_by('-created_at')[:5].values(
            'id', 'user__email', 'total_amount', 'status', 'created_at'
        )

        return Response({
            "total_sales": total_sales,
            "total_orders": total_orders,
            "total_users": total_users,
            "low_stock_count": low_stock_products,
            "recent_orders": recent_orders
        })



class AdminAnalyticsView(APIView):
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAdminUser]
    renderer_classes = [renderers.TemplateHTMLRenderer]
    template_name = 'admin/analytics_dashboard.html'

    def get(self, request):
        # 1. Top 10 Customers
        top_customers = User.objects.annotate(
            total_spent=Sum('orders__total_amount')
        ).order_by('-total_spent')[:10].values('email', 'total_spent')

        # 2. Monthly Sales (Last 6 Months)
        six_months_ago = now() - timedelta(days=180)
        monthly_sales = Order.objects.filter(created_at__gte=six_months_ago).annotate(
            period=TruncMonth('created_at')
        ).values('period').annotate(
            total=Sum('total_amount')
        ).order_by('period')
        
        # Format dates for JS
        monthly_sales_formatted = [
            {'period': x['period'].strftime('%Y-%m'), 'total': float(x['total'])} 
            for x in monthly_sales
        ]

        # 3. Top Products
        top_products = Product.objects.annotate(
            sold_count=Sum('order_items__quantity')
        ).order_by('-sold_count')[:10].values('name', 'sold_count')

        # 4. Order Status
        order_status = Order.objects.values('status').annotate(
            count=Count('id')
        )

        # 5. Orders per Branch
        branch_sales = Order.objects.exclude(branch__isnull=True).values('branch__name').annotate(
            count=Count('id')
        ).order_by('-count')

        context = {
            'top_customers': json.dumps(list(top_customers), cls=DjangoJSONEncoder),
            'monthly_sales': json.dumps(monthly_sales_formatted, cls=DjangoJSONEncoder),
            'top_products': json.dumps([{'name': p['name'], 'count': p['sold_count'] or 0} for p in top_products], cls=DjangoJSONEncoder),
            'order_status': json.dumps(list(order_status), cls=DjangoJSONEncoder),
            'branch_sales': json.dumps(list(branch_sales), cls=DjangoJSONEncoder),
        }
        return Response(context)
