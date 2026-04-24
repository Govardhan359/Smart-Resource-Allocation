from django.db import models
from volunteers.models import Volunteer
from needs.models import Need

class Assignment(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('declined', 'Declined'),
        ('completed', 'Completed'),
    ]
    volunteer = models.ForeignKey(Volunteer, on_delete=models.CASCADE)
    need = models.ForeignKey(Need, on_delete=models.CASCADE)
    match_score = models.FloatField(default=0.0)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    assigned_at = models.DateTimeField(auto_now_add=True)
    responded_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.volunteer.name} → {self.need.title} ({self.status})"