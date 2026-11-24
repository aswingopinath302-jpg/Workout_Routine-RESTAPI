from django.db import models
from django.db import models
from django.contrib.auth.models import User


class WorkoutSession(models.Model):
    CATEGORY_CHOICES = [
        ('PUSH', 'Push'),
        ('PULL', 'Pull'),
        ('LEGS', 'Legs'),
        ('CARDIO', 'Cardio'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    category = models.CharField(max_length=10, choices=CATEGORY_CHOICES)
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.user.username} - {self.category} ({self.date})"
