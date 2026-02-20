from datetime import timedelta

from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    is_premium = models.BooleanField(default=False)
    premium_until = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.user.username} Profile"

    def upgrade_to_premium(self, days=30):
        self.is_premium = True
        self.premium_until = timezone.now() + timedelta(days=days)
        self.save(update_fields=["is_premium", "premium_until"])
