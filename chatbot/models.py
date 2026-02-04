# chatbot/models.py
from django.db import models
from django.contrib.auth.models import User

class ChatMessage(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='chat_messages')
    message = models.TextField()
    is_user = models.BooleanField(default=True)  # True if user, False if bot
    mood_context = models.CharField(max_length=20, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['created_at']
    
    def __str__(self):
        sender = "User" if self.is_user else "Bot"
        return f"{self.user.username} - {sender}: {self.message[:50]}"