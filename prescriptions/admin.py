from django.contrib import admin
from django.utils.html import format_html
from .models import Prescription

@admin.register(Prescription)
class PrescriptionAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'status', 'created_at', 'image_preview')
    list_filter = ('status', 'created_at')
    search_fields = ('user__email', 'id')
    readonly_fields = ('created_at',)
    list_editable = ('status',)

    def image_preview(self, obj):
        if obj.image:
            return format_html('<a href="{}" target="_blank"><img src="{}" style="width: 50px; height: 50px; object-fit: cover;" /></a>', obj.image.url, obj.image.url)
        return "No Image"
    image_preview.short_description = 'Image'
