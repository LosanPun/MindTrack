import json
from django.contrib import admin
from django.contrib.admin.sites import NotRegistered
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group, User
from django.utils.text import Truncator

from analysis.models import MoodAnalysis
from chatbot.models import ChatMessage, UserChatSession

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


class UserChatSessionInline(admin.StackedInline):
    model = UserChatSession
    extra = 0
    can_delete = False
    show_change_link = True
    fields = (
        "current_mood",
        "last_intent",
        "conversation_topic",
        "interaction_count",
        "context_pretty",
        "created_at",
        "updated_at",
    )
    readonly_fields = ("context_pretty", "created_at", "updated_at")

    def context_pretty(self, obj):
        if not obj or not obj.context_data:
            return "-"
        return json.dumps(obj.context_data, indent=2, ensure_ascii=True)

    context_pretty.short_description = "Context Data"


class MoodAnalysisInline(admin.TabularInline):
    model = MoodAnalysis
    extra = 0
    can_delete = False
    show_change_link = True
    fields = ("created_at", "detected_mood", "confidence", "text_preview")
    readonly_fields = ("created_at", "detected_mood", "confidence", "text_preview")
    ordering = ("-created_at",)

    def text_preview(self, obj):
        return Truncator(obj.text).chars(80)

    text_preview.short_description = "Text"


class ChatMessageInline(admin.TabularInline):
    model = ChatMessage
    extra = 0
    can_delete = False
    show_change_link = True
    fields = ("created_at", "is_user", "mood_context", "intent_detected", "message_preview")
    readonly_fields = ("created_at", "is_user", "mood_context", "intent_detected", "message_preview")
    ordering = ("-created_at",)

    def message_preview(self, obj):
        return Truncator(obj.message).chars(80)

    message_preview.short_description = "Message"


try:
    admin.site.unregister(User)
except NotRegistered:
    pass


@admin.register(User)
class UserAdmin(StaffRoleGuardMixin, BaseUserAdmin):
    list_display = ("username", "email", "first_name", "last_name", "is_staff", "is_active", "date_joined")
    list_filter = ("is_staff", "is_superuser", "is_active", "groups")
    inlines = (UserChatSessionInline, MoodAnalysisInline, ChatMessageInline)
    actions = ("assign_viewer_role", "assign_editor_role")

    @admin.action(description="Assign selected users to MindTrack Viewers")
    def assign_viewer_role(self, request, queryset):
        viewer_group, _ = Group.objects.get_or_create(name=VIEWER_GROUP_NAME)
        editor_group = Group.objects.filter(name=EDITOR_GROUP_NAME).first()
        updated = 0
        for user in queryset:
            user.groups.add(viewer_group)
            if editor_group:
                user.groups.remove(editor_group)
            updated += 1
        self.message_user(request, f"{updated} user(s) assigned to {VIEWER_GROUP_NAME}.")

    @admin.action(description="Assign selected users to MindTrack Editors")
    def assign_editor_role(self, request, queryset):
        editor_group, _ = Group.objects.get_or_create(name=EDITOR_GROUP_NAME)
        viewer_group = Group.objects.filter(name=VIEWER_GROUP_NAME).first()
        updated = 0
        for user in queryset:
            user.groups.add(editor_group)
            if viewer_group:
                user.groups.remove(viewer_group)
            updated += 1
        self.message_user(request, f"{updated} user(s) assigned to {EDITOR_GROUP_NAME}.")
