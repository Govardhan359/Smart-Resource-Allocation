from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import viewsets
from django.utils import timezone
from .models import Assignment
from .serializers import AssignmentSerializer
from needs.models import Need
from volunteers.models import Volunteer

class AssignmentViewSet(viewsets.ModelViewSet):
    queryset = Assignment.objects.select_related('volunteer', 'need').all().order_by('-assigned_at')
    serializer_class = AssignmentSerializer

class AssignVolunteerView(APIView):
    def post(self, request):
        need_id = request.data.get('need_id')
        volunteer_id = request.data.get('volunteer_id')
        score = request.data.get('match_score', 0.0)

        try:
            need = Need.objects.get(id=need_id)
            volunteer = Volunteer.objects.get(id=volunteer_id)
        except (Need.DoesNotExist, Volunteer.DoesNotExist):
            return Response({'error': 'Need or Volunteer not found'}, status=404)

        assignment = Assignment.objects.create(
            need=need,
            volunteer=volunteer,
            match_score=score,
            status='pending'
        )
        need.status = 'assigned'
        need.save()

        return Response({
            'message': 'Volunteer assigned successfully',
            'assignment_id': assignment.id,
            'volunteer': volunteer.name,
            'need': need.title,
            'status': assignment.status
        }, status=201)

class RespondAssignmentView(APIView):
    def post(self, request, assignment_id):
        # Accept both 'action' and 'response' keys, both value formats
        action = request.data.get('action') or request.data.get('response')

        # Normalize: "accepted" → "accept", "declined" → "decline"
        if action in ('accepted', 'accept'):
            action = 'accept'
        elif action in ('declined', 'decline'):
            action = 'decline'

        try:
            assignment = Assignment.objects.get(id=assignment_id)
        except Assignment.DoesNotExist:
            return Response({'error': 'Assignment not found'}, status=404)

        if action == 'accept':
            assignment.status = 'accepted'
        elif action == 'decline':
            assignment.status = 'declined'
            assignment.need.status = 'open'
            assignment.need.save()
        else:
            return Response({'error': 'Invalid action'}, status=400)

        assignment.responded_at = timezone.now()
        assignment.save()

        return Response({
            'message': f'Assignment {action}ed successfully',
            'assignment_id': assignment.id,
            'status': assignment.status
        })