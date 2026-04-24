from django.contrib import admin
from .models import Need

@admin.register(Need)
class NeedAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'urgency_score', 'area_name', 'status', 'created_at']
    list_filter = ['category', 'status']
    search_fields = ['title', 'area_name']