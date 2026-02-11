from django.contrib import admin

from .models import ChatMessage

@admin.register(ChatMessage)
class ChatMessageAdmin(admin.ModelAdmin):
    list_display = ('user', 'message', 'is_user', 'created_at')
    list_filter = ('is_user', 'created_at')
    search_fields = ('message',)

