from rest_framework.views import APIView
from rest_framework.response import Response
from needs.models import Need
from volunteers.models import Volunteer
from dispatch.models import Assignment
from django.db.models import Count, Avg

class DashboardStatsView(APIView):
    def get(self, request):
        total_needs = Need.objects.count()
        open_needs = Need.objects.filter(status='open').count()
        assigned_needs = Need.objects.filter(status='assigned').count()
        resolved_needs = Need.objects.filter(status='resolved').count()
        total_volunteers = Volunteer.objects.count()
        available_volunteers = Volunteer.objects.filter(available=True).count()
        total_assignments = Assignment.objects.count()
        accepted = Assignment.objects.filter(status='accepted').count()

        needs_by_category = list(
            Need.objects.values('category')
            .annotate(count=Count('id'))
            .order_by('-count')
        )

        urgent_needs = list(
            Need.objects.filter(status='open')
            .order_by('-urgency_score')
            .values('id', 'title', 'category', 'urgency_score', 'area_name')[:5]
        )

        return Response({
            'needs': {
                'total': total_needs,
                'open': open_needs,
                'assigned': assigned_needs,
                'resolved': resolved_needs,
                'by_category': needs_by_category,
            },
            'volunteers': {
                'total': total_volunteers,
                'available': available_volunteers,
            },
            'assignments': {
                'total': total_assignments,
                'accepted': accepted,
            },
            'urgent_needs': urgent_needs,
        })