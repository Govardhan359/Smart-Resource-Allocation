from rest_framework import viewsets
from .models import Need
from .serializers import NeedSerializer

class NeedViewSet(viewsets.ModelViewSet):
    queryset = Need.objects.all().order_by('-urgency_score')
    serializer_class = NeedSerializer
