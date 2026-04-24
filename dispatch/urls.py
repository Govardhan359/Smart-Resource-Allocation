from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AssignmentViewSet, AssignVolunteerView, RespondAssignmentView

router = DefaultRouter()
router.register(r'assignments', AssignmentViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('assign/', AssignVolunteerView.as_view(), name='assign-volunteer'),
    path('respond/<int:assignment_id>/', RespondAssignmentView.as_view(), name='respond-assignment'),
]