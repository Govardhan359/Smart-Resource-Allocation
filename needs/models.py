from django.db import models

class Need(models.Model):
    CATEGORY_CHOICES = [
        ('food', 'Food'),
        ('medical', 'Medical'),
        ('shelter', 'Shelter'),
        ('education', 'Education'),
        ('other', 'Other'),
    ]
    STATUS_CHOICES = [
        ('open', 'Open'),
        ('assigned', 'Assigned'),
        ('resolved', 'Resolved'),
    ]
    title = models.CharField(max_length=300)
    description = models.TextField()
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    urgency_score = models.FloatField(default=0.0)
    location_lat = models.FloatField(default=0.0)
    location_lng = models.FloatField(default=0.0)
    area_name = models.CharField(max_length=200, default='')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='open')
    source_text = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.category} - {self.area_name} (urgency: {self.urgency_score})"