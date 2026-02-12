from django.contrib import admin

<<<<<<< HEAD
from .models import ChatMessage

@admin.register(ChatMessage)
class ChatMessageAdmin(admin.ModelAdmin):
    list_display = ('user', 'message', 'is_user', 'created_at')
    list_filter = ('is_user', 'created_at')
    search_fields = ('message',)
=======
# from .models import MoodEntry, Subscription

# @admin.register(MoodEntry)
# class MoodEntryAdmin(admin.ModelAdmin):
#     list_display = ('user', 'detected_mood', 'confidence_score', 'created_at')
#     list_filter = ('detected_mood', 'created_at')
#     search_fields = ('text',)

# @admin.register(Subscription)
# class SubscriptionAdmin(admin.ModelAdmin):
#     list_display = ('user', 'plan', 'is_active', 'mood_analysis_used', 'subscribed_on')
#     list_filter = ('plan', 'is_active')



# from .models import TestModel

# admin.site.register(TestModel)
>>>>>>> javicmusk

