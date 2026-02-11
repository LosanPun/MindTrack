# chatbot/models.py
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class ChatMessage(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='chat_messages')
    message = models.TextField()
    is_user = models.BooleanField(default=True)
    mood_context = models.CharField(max_length=50, blank=True, null=True)
    intent_detected = models.CharField(max_length=50, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        sender = "User" if self.is_user else "Bot"
        return f"{self.user.username} - {sender}: {self.message[:50]}"

class UserChatSession(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='chat_session')
    current_mood = models.CharField(max_length=50, blank=True, null=True)
    last_interaction = models.DateTimeField(blank=True, null=True)
    interaction_count = models.IntegerField(default=0)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} - Session"
