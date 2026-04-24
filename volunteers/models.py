from django.db import models

class Volunteer(models.Model):
    name = models.CharField(max_length=200)
    phone = models.CharField(max_length=20)
    email = models.EmailField(unique=True)
    skills = models.JSONField(default=list)
    location_lat = models.FloatField(default=0.0)
    location_lng = models.FloatField(default=0.0)
    area_name = models.CharField(max_length=200, default='')
    available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name