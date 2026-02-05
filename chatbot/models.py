# chatbot/models.py
from django.db import models
from django.contrib.auth.models import User

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
    """Tracks user's conversation state"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='chat_session')
    current_mood = models.CharField(max_length=50, blank=True, null=True)
    last_intent = models.CharField(max_length=50, blank=True, null=True)
    conversation_topic = models.CharField(max_length=100, blank=True, null=True)
    interaction_count = models.IntegerField(default=0)
    last_interaction = models.DateTimeField(auto_now=True)
    context_data = models.JSONField(default=dict)
    
    def __str__(self):
        return f"{self.user.username} - Session"
    
    def get_context_data(self):
        """Get context data with defaults"""
        default_data = {
            'last_quotes_given': [],
            'last_songs_given': [],
            'last_poems_given': [],
            'last_exercise_tips_given': [],
            'cheer_up_context': False,
            'recent_moods': []
        }
        
        # Merge with existing data
        context_data = {**default_data, **self.context_data}
        self.context_data = context_data
        self.save()
        return context_data
    
    def update_context_data(self, updates):
        """Update context data"""
        context_data = self.get_context_data()
        context_data.update(updates)
        self.context_data = context_data
        self.save()