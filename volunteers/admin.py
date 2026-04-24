from django.contrib import admin
from .models import Volunteer

@admin.register(Volunteer)
class VolunteerAdmin(admin.ModelAdmin):
    list_display = ['name', 'phone', 'email', 'area_name', 'available', 'created_at']
    list_filter = ['available', 'area_name']
    search_fields = ['name', 'email', 'phone']