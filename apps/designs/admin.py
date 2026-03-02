from django.contrib import admin
from .models import Design

@admin.register(Design)
class DesignAdmin(admin.ModelAdmin):
    list_display = ['title', 'tailor', 'clothing_type', 'price', 'is_available', 'created_at']
    list_filter = ['clothing_type', 'is_available']
    search_fields = ['title', 'tailor__username']
