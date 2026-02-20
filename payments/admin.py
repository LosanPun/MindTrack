from django.contrib import admin

from .models import KhaltiPayment


@admin.register(KhaltiPayment)
class KhaltiPaymentAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user",
        "amount",
        "total_amount",
        "status",
        "transaction_id",
        "refunded",
        "created_at",
    )
    list_filter = ("status", "refunded", "created_at")
    search_fields = ("pidx", "transaction_id", "purchase_order_id", "user__username", "user__email")
    readonly_fields = ("pidx", "transaction_id", "amount", "total_amount", "fee", "created_at", "updated_at")
