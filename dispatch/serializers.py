from rest_framework import serializers
from .models import Assignment

class AssignmentSerializer(serializers.ModelSerializer):
    volunteer_name = serializers.CharField(source='volunteer.name', read_only=True)
    need_title = serializers.CharField(source='need.title', read_only=True)

    class Meta:
        model = Assignment
        fields = ['id', 'volunteer_name', 'need_title', 'match_score', 'status', 'assigned_at']