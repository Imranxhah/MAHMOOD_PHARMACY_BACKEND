from django.contrib import admin
from .models import Order, OrderItem, DeliveryCharge

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    readonly_fields = ('product', 'quantity', 'price_at_purchase')
    can_delete = False
    extra = 0

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('user', 'branch', 'status', 'payment_method', 'total_amount', 'order_at')
    search_fields = ('user__email', 'id', 'contact_number')

    def get_list_filter(self, request):
        if request.user.is_superuser:
            return ('status', 'created_at', 'payment_method', 'branch')
        return ('status', 'created_at', 'payment_method')
    readonly_fields = ('total_amount',)
    inlines = [OrderItemInline]
    list_editable = ('status',)
    list_display_links = ('user',)

    def order_at(self, obj):
        return obj.created_at
    order_at.short_description = 'Order At'
    order_at.admin_order_field = 'created_at'

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        if request.user.branch:
            return qs.filter(branch=request.user.branch)
        return qs

@admin.register(DeliveryCharge)
class DeliveryChargeAdmin(admin.ModelAdmin):
    list_display = ('amount', 'updated_at')
    # Limit to one object in Admin? Not strictly asked but good practice for singleton. 
    # But user said "if there are multiple object in that model return the first one only than", 
    # so standard admin is fine.
