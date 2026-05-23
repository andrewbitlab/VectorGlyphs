from __future__ import annotations

import secrets
from dataclasses import dataclass
from hashlib import sha256
from typing import Any

from app.payments.repository import OrderRecord, PaymentRepository
from app.settings import Settings


@dataclass(frozen=True)
class CheckoutResult:
    order: OrderRecord
    checkout_session_id: str
    checkout_url: str


def _id(prefix: str, payload: str) -> str:
    return f"{prefix}_{sha256((payload + secrets.token_urlsafe(16)).encode('utf-8')).hexdigest()[:24]}"


def create_checkout_session(payload: dict[str, Any], *, settings: Settings) -> CheckoutResult:
    settings.validate_payment_ready()
    repo = PaymentRepository(settings.payment_db_path)
    order_id = _id("ord", repr(sorted(payload.items())))
    checkout_session_id = _id("cs_test", order_id)
    order = repo.create_order(
        order_id=order_id,
        checkout_session_id=checkout_session_id,
        amount_cents=settings.export_pack_amount_cents,
        currency=settings.currency,
        customer_email=payload.get("customerEmail"),
        spec_payload=payload,
    )
    checkout_url = f"https://checkout.stripe.com/c/pay/{checkout_session_id}"
    return CheckoutResult(order=order, checkout_session_id=checkout_session_id, checkout_url=checkout_url)
