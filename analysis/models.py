# analysis/models.py
from django.db import models
from django.contrib.auth.models import User

class MoodAnalysis(models.Model):
    MOOD_CHOICES = [
        ('happy', '😊 Happy'),
        ('sad', '😢 Sad'),
        ('angry', '😠 Angry'),
        ('fear', '😨 Fear'),
        ('neutral', '😐 Neutral'),
        ('surprise', '😲 Surprise'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='mood_analyses')
    text = models.TextField()
    detected_mood = models.CharField(max_length=20, choices=MOOD_CHOICES)
    confidence = models.FloatField(default=0.0)
    emotions = models.JSONField(default=dict)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.user.username} - {self.detected_mood} ({self.confidence:.0%})"
    
    class Meta:
        verbose_name_plural = "Mood Analyses"
        ordering = ['-created_at']