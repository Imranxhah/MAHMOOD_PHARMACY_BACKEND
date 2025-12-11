from django.contrib import admin
from .models import Order, OrderItem

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    readonly_fields = ('product', 'quantity', 'price_at_purchase')
    can_delete = False
    extra = 0

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('user', 'branch', 'status', 'payment_method', 'total_amount', 'order_at')
    list_filter = ('status', 'created_at', 'payment_method', 'branch')
    search_fields = ('user__email', 'id', 'contact_number')
    readonly_fields = ('total_amount',)
    inlines = [OrderItemInline]
    list_editable = ('status',)
    list_display_links = ('user', 'branch', 'payment_method', 'total_amount', 'order_at')

    def order_at(self, obj):
        return obj.created_at
    order_at.short_description = 'Order At'
    order_at.admin_order_field = 'created_at'
