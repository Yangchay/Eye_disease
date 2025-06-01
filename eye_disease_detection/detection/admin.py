from django.contrib import admin
from .models import Detection

@admin.register(Detection)
class DetectionAdmin(admin.ModelAdmin):
    list_display = ['prediction', 'confidence', 'created_at']
    list_filter = ['prediction', 'created_at']
    readonly_fields = ['created_at']
    ordering = ['-created_at']