from rest_framework.views import APIView
from rest_framework.response import Response
from .engine import match_volunteers_to_need
from needs.models import Need
from needs.serializers import NeedSerializer

class MatchVolunteersView(APIView):
    def get(self, request, need_id):
        matches = match_volunteers_to_need(need_id)
        if not matches:
            return Response({'error': 'Need not found or no volunteers available'}, status=404)
        return Response({
            'need_id': need_id,
            'matches': matches
        })

class OpenNeedsView(APIView):
    def get(self, request):
        needs = Need.objects.filter(status='open').order_by('-urgency_score')
        serializer = NeedSerializer(needs, many=True)
        return Response(serializer.data)