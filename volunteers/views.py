from django.shortcuts import render
from rest_framework import viewsets
from .models import Volunteer
from .serializers import VolunteerSerializer

class VolunteerViewSet(viewsets.ModelViewSet):
    queryset = Volunteer.objects.all()
    serializer_class = VolunteerSerializer