from __future__ import annotations

import hmac
import json
from hashlib import sha256
from time import time
from typing import Any


class WebhookSignatureError(ValueError):
    pass


def _parse_signature_header(header: str) -> tuple[int, list[str]]:
    timestamp: int | None = None
    signatures: list[str] = []
    for item in header.split(","):
        if "=" not in item:
            continue
        key, value = item.split("=", 1)
        if key == "t":
            try:
                timestamp = int(value)
            except ValueError as exc:  # pragma: no cover - defensive
                raise WebhookSignatureError("invalid Stripe signature timestamp") from exc
        elif key == "v1":
            signatures.append(value)
    if timestamp is None or not signatures:
        raise WebhookSignatureError("missing Stripe signature timestamp or digest")
    return timestamp, signatures


def verify_stripe_webhook(payload: bytes, signature_header: str, secret: str, tolerance_seconds: int = 300) -> dict[str, Any]:
    if not secret.startswith("whsec_"):
        raise WebhookSignatureError("Stripe webhook secret must be configured")
    timestamp, signatures = _parse_signature_header(signature_header)
    if abs(int(time()) - timestamp) > tolerance_seconds:
        raise WebhookSignatureError("Stripe webhook signature timestamp is outside tolerance")
    signed_payload = f"{timestamp}.".encode("utf-8") + payload
    expected = hmac.new(secret.encode("utf-8"), signed_payload, sha256).hexdigest()
    if not any(hmac.compare_digest(expected, signature) for signature in signatures):
        raise WebhookSignatureError("invalid Stripe webhook signature")
    return json.loads(payload.decode("utf-8"))
