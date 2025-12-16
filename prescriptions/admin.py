from django.contrib import admin
from django.utils.html import format_html
from .models import Prescription

@admin.register(Prescription)
class PrescriptionAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'branch', 'status', 'created_at', 'image_preview')
    def get_list_filter(self, request):
        if request.user.is_superuser:
            return ('status', 'branch', 'created_at')
        return ('status', 'created_at')

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        if request.user.branch:
            return qs.filter(branch=request.user.branch)
        return qs
    search_fields = ('user__email', 'id')
    readonly_fields = ('created_at',)
    list_editable = ('status',)

    def image_preview(self, obj):
        if obj.image:
            return format_html('<a href="{}" target="_blank"><img src="{}" style="width: 50px; height: 50px; object-fit: cover;" /></a>', obj.image.url, obj.image.url)
        return "No Image"
    image_preview.short_description = 'Image'

    def save_model(self, request, obj, form, change):
        if not request.user.is_superuser and request.user.branch:
            obj.branch = request.user.branch
        super().save_model(request, obj, form, change)

    def get_readonly_fields(self, request, obj=None):
        if not request.user.is_superuser and request.user.branch:
            return self.readonly_fields + ('branch',)
        return self.readonly_fields
