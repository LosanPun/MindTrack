from django.conf import settings
from django.db import models


class PaymentStatus(models.TextChoices):
    PENDING = "Pending", "Pending"
    COMPLETED = "Completed", "Completed"
    FAILED = "Failed", "Failed"
    REFUNDED = "Refunded", "Refunded"


class KhaltiPayment(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="khalti_payments",
    )
    pidx = models.CharField(max_length=255, unique=True)
    purchase_order_id = models.CharField(max_length=255, null=True, blank=True)
    purchase_order_name = models.CharField(max_length=255, null=True, blank=True)
    transaction_id = models.CharField(max_length=255, null=True, blank=True)
    amount = models.PositiveIntegerField()
    total_amount = models.PositiveIntegerField(null=True, blank=True)
    status = models.CharField(
        max_length=20,
        choices=PaymentStatus.choices,
        default=PaymentStatus.PENDING,
    )
    fee = models.PositiveIntegerField(default=0)
    refunded = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["status"]),
            models.Index(fields=["created_at"]),
            models.Index(fields=["transaction_id"]),
        ]

    def __str__(self):
        return self.pidx
