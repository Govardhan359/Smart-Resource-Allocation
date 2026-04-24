from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/volunteers/', include('volunteers.urls')),
    path('api/needs/', include('needs.urls')),
    path('api/dispatch/', include('dispatch.urls')),
    path('api/matching/', include('matching.urls')),
    path('api/dashboard/', include('dashboard.urls')),
    path('api/ingestion/', include('ingestion.urls')),
]