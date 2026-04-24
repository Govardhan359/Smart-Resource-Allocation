from django.urls import path
from .views import MatchVolunteersView, OpenNeedsView

urlpatterns = [
    path('match/<int:need_id>/', MatchVolunteersView.as_view(), name='match-volunteers'),
    path('open-needs/', OpenNeedsView.as_view(), name='open-needs'),
]