from django.contrib import admin
from django.http import HttpResponse
import csv
from .models import MoodAnalysis

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


@admin.register(MoodAnalysis)
class MoodAnalysisAdmin(StaffRoleGuardMixin, admin.ModelAdmin):
    list_display = ("id", "user", "detected_mood", "confidence", "created_at")
    list_filter = ("detected_mood", "created_at")
    search_fields = ("user__username", "user__email", "text")
    ordering = ("-created_at",)
    date_hierarchy = "created_at"
    readonly_fields = ("created_at",)
    actions = ("export_selected_as_csv",)

    @admin.action(description="Export selected mood analyses as CSV")
    def export_selected_as_csv(self, request, queryset):
        response = HttpResponse(content_type="text/csv")
        response["Content-Disposition"] = 'attachment; filename="mood_analyses.csv"'

        writer = csv.writer(response)
        writer.writerow(["id", "user", "detected_mood", "confidence", "created_at", "text"])

        for analysis in queryset.select_related("user"):
            writer.writerow(
                [
                    analysis.id,
                    analysis.user.username,
                    analysis.detected_mood,
                    analysis.confidence,
                    analysis.created_at.isoformat(),
                    analysis.text,
                ]
            )

        return response
