from django.contrib.auth.models import Group, Permission
from django.db.models.signals import post_migrate
from django.dispatch import receiver

VIEWER_GROUP_NAME = "MindTrack Viewers"
EDITOR_GROUP_NAME = "MindTrack Editors"

# (app_label, model_name): (viewer_actions, editor_actions)
PERMISSION_MATRIX = {
    ("analysis", "moodanalysis"): (["view"], ["view", "add", "change", "delete"]),
    ("chatbot", "chatmessage"): (["view"], ["view", "add", "change", "delete"]),
    ("chatbot", "userchatsession"): (["view"], ["view", "add", "change", "delete"]),
    ("auth", "user"): (["view"], ["view", "change"]),
}


def _collect_permissions():
    viewer_permissions = []
    editor_permissions = []

    for (app_label, model_name), (viewer_actions, editor_actions) in PERMISSION_MATRIX.items():
        for action in viewer_actions:
            codename = f"{action}_{model_name}"
            permission = Permission.objects.filter(
                content_type__app_label=app_label,
                codename=codename,
            ).first()
            if permission:
                viewer_permissions.append(permission)

        for action in editor_actions:
            codename = f"{action}_{model_name}"
            permission = Permission.objects.filter(
                content_type__app_label=app_label,
                codename=codename,
            ).first()
            if permission:
                editor_permissions.append(permission)

    return viewer_permissions, editor_permissions


@receiver(post_migrate)
def create_or_update_staff_groups(sender, **kwargs):
    viewer_group, _ = Group.objects.get_or_create(name=VIEWER_GROUP_NAME)
    editor_group, _ = Group.objects.get_or_create(name=EDITOR_GROUP_NAME)

    viewer_permissions, editor_permissions = _collect_permissions()
    viewer_group.permissions.set(viewer_permissions)
    editor_group.permissions.set(editor_permissions)
