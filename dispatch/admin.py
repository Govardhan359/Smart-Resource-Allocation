from django.contrib import admin
from .models import Assignment

@admin.register(Assignment)
class AssignmentAdmin(admin.ModelAdmin):
    list_display = ['volunteer', 'need', 'match_score', 'status', 'assigned_at']
    list_filter = ['status']