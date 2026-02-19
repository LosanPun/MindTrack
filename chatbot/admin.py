from django.contrib import admin
import csv
from django.http import HttpResponse
from .models import ChatMessage, UserChatSession

VIEWER_GROUP_NAME = "MindTrack Viewers"
EDITOR_GROUP_NAME = "MindTrack Editors"


class StaffRoleGuardMixin:
    def _is_viewer(self, user):
        return user.is_authenticated and user.groups.filter(name=VIEWER_GROUP_NAME).exists()

    def _is_editor(self, user):
        return user.is_authenticated and user.groups.filter(name=EDITOR_GROUP_NAME).exists()

    def has_module_permission(self, request):
        if request.user.is_superuser or self._is_editor(request.user):
            return super().has_module_permission(request)
        if self._is_viewer(request.user):
            return True
        return super().has_module_permission(request)

    def has_view_permission(self, request, obj=None):
        if request.user.is_superuser or self._is_editor(request.user):
            return super().has_view_permission(request, obj)
        if self._is_viewer(request.user):
            return True
        return super().has_view_permission(request, obj)

    def has_add_permission(self, request):
        if self._is_viewer(request.user) and not self._is_editor(request.user):
            return False
        return super().has_add_permission(request)

    def has_change_permission(self, request, obj=None):
        if self._is_viewer(request.user) and not self._is_editor(request.user):
            return False
        return super().has_change_permission(request, obj)

    def has_delete_permission(self, request, obj=None):
        if self._is_viewer(request.user) and not self._is_editor(request.user):
            return False
        return super().has_delete_permission(request, obj)


@admin.register(ChatMessage)
class ChatMessageAdmin(StaffRoleGuardMixin, admin.ModelAdmin):
    list_display = (
        "id",
        "user",
        "is_user",
        "mood_context",
        "intent_detected",
        "created_at",
    )
    list_filter = ("is_user", "mood_context", "intent_detected", "created_at")
    search_fields = ("user__username", "user__email", "message")
    ordering = ("-created_at",)
    date_hierarchy = "created_at"
    readonly_fields = ("created_at",)
    actions = ("mark_selected_as_user_messages", "mark_selected_as_bot_messages", "export_selected_as_csv")

    @admin.action(description="Mark selected as user messages")
    def mark_selected_as_user_messages(self, request, queryset):
        updated = queryset.update(is_user=True)
        self.message_user(request, f"{updated} message(s) marked as user.")

    @admin.action(description="Mark selected as bot messages")
    def mark_selected_as_bot_messages(self, request, queryset):
        updated = queryset.update(is_user=False)
        self.message_user(request, f"{updated} message(s) marked as bot.")

    @admin.action(description="Export selected chat messages as CSV")
    def export_selected_as_csv(self, request, queryset):
        response = HttpResponse(content_type="text/csv")
        response["Content-Disposition"] = 'attachment; filename="chat_messages.csv"'

        writer = csv.writer(response)
        writer.writerow(
            [
                "id",
                "user",
                "is_user",
                "mood_context",
                "intent_detected",
                "created_at",
                "message",
            ]
        )

        for message in queryset.select_related("user"):
            writer.writerow(
                [
                    message.id,
                    message.user.username,
                    message.is_user,
                    message.mood_context or "",
                    message.intent_detected or "",
                    message.created_at.isoformat(),
                    message.message,
                ]
            )

        return response


@admin.register(UserChatSession)
class UserChatSessionAdmin(StaffRoleGuardMixin, admin.ModelAdmin):
    list_display = (
        "id",
        "user",
        "current_mood",
        "last_intent",
        "conversation_topic",
        "interaction_count",
        "updated_at",
    )
    list_filter = ("current_mood", "last_intent", "updated_at")
    search_fields = ("user__username", "user__email", "conversation_topic")
    ordering = ("-updated_at",)
    readonly_fields = ("created_at", "updated_at")

