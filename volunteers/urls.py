from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import VolunteerViewSet

router = DefaultRouter()
router.register(r'', VolunteerViewSet)

urlpatterns = [
    path('', include(router.urls)),
]