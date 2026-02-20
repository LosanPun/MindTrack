from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import render
from django.urls import reverse
from urllib.parse import urljoin
from django.views.decorators.http import require_GET, require_POST

import requests
import uuid

from .models import KhaltiPayment, PaymentStatus


KHALTI_INITIATE_URL = "https://dev.khalti.com/api/v2/epayment/initiate/"
KHALTI_LOOKUP_URL = "https://dev.khalti.com/api/v2/epayment/lookup/"


def _safe_upgrade_user(user):
    if not user:
        return

    profile = getattr(user, "profile", None)
    if profile and hasattr(profile, "upgrade_to_premium"):
        profile.upgrade_to_premium(days=30)


@require_POST
def khalti_initiate(request):
    if not settings.KHALTI_SECRET_KEY:
        return JsonResponse({"error": "Khalti secret key is not configured."}, status=500)

    amount = 1000
    purchase_order_id = str(uuid.uuid4())
    purchase_order_name = "MindTrack Upgrade"

    site_url = getattr(settings, "SITE_URL", "http://127.0.0.1:8000")
    website_url = site_url.rstrip("/") + "/"
    return_url = urljoin(website_url, reverse("payments:khalti_callback").lstrip("/"))

    payload = {
        "return_url": return_url,
        "website_url": website_url,
        "amount": amount,
        "purchase_order_id": purchase_order_id,
        "purchase_order_name": purchase_order_name,
        "customer_info": {
            "name": request.user.username if request.user.is_authenticated else "MindTrack User",
            "email": request.user.email if request.user.is_authenticated else "test@example.com",
            "phone": "9800000000",
        },
    }

    headers = {
        "Authorization": f"Key {settings.KHALTI_SECRET_KEY}",
        "Content-Type": "application/json",
    }

    try:
        response = requests.post(
            KHALTI_INITIATE_URL,
            json=payload,
            headers=headers,
            timeout=15,
        )
        response.raise_for_status()
        data = response.json()
    except requests.RequestException as exc:
        return JsonResponse({"error": f"Khalti initiate failed: {exc}"}, status=502)

    pidx = data.get("pidx")
    payment_url = data.get("payment_url")

    if not pidx or not payment_url:
        return JsonResponse({"error": "Invalid response from Khalti."}, status=502)

    KhaltiPayment.objects.update_or_create(
        pidx=pidx,
        defaults={
            "user": request.user if request.user.is_authenticated else None,
            "purchase_order_id": purchase_order_id,
            "purchase_order_name": purchase_order_name,
            "amount": amount,
            "status": PaymentStatus.PENDING,
        },
    )

    return JsonResponse({"pidx": pidx, "payment_url": payment_url})


@require_GET
def khalti_callback(request):
    if not settings.KHALTI_SECRET_KEY:
        return JsonResponse({"error": "Khalti secret key is not configured."}, status=500)

    pidx = request.GET.get("pidx")
    if not pidx:
        return JsonResponse({"error": "No pidx found in callback."}, status=400)

    headers = {"Authorization": f"Key {settings.KHALTI_SECRET_KEY}"}

    try:
        response = requests.post(
            KHALTI_LOOKUP_URL,
            json={"pidx": pidx},
            headers=headers,
            timeout=15,
        )
        data = response.json()
    except requests.RequestException as exc:
        return JsonResponse({"error": f"Khalti lookup failed: {exc}"}, status=502)

    payment = KhaltiPayment.objects.filter(pidx=pidx).first()

    if response.status_code == 200 and data.get("status") == PaymentStatus.COMPLETED:
        received_amount = data.get("total_amount") or data.get("amount")
        if payment and received_amount and payment.amount != int(received_amount):
            return render(request, "payments/payment_failure.html", {"data": data, "reason": "Amount mismatch"}, status=400)

        was_completed = bool(payment and payment.status == PaymentStatus.COMPLETED)
        if not payment:
            payment = KhaltiPayment(pidx=pidx, amount=int(received_amount or 0))

        payment.user = payment.user or (request.user if request.user.is_authenticated else None)
        payment.transaction_id = data.get("transaction_id", "")
        payment.total_amount = data.get("total_amount") or data.get("amount") or 0
        payment.status = data.get("status", PaymentStatus.COMPLETED)
        payment.fee = data.get("fee") or 0
        payment.refunded = bool(data.get("refunded", False))
        payment.purchase_order_id = data.get("purchase_order_id")
        payment.purchase_order_name = data.get("purchase_order_name")
        payment.save()

        if not was_completed:
            _safe_upgrade_user(payment.user)

        return render(request, "payments/payment_success.html", {"data": data})

    if payment:
        payment.status = data.get("status", PaymentStatus.FAILED)
        payment.save(update_fields=["status", "updated_at"])

    return render(request, "payments/payment_failure.html", {"data": data}, status=400)
