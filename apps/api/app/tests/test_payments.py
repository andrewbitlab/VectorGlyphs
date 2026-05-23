from __future__ import annotations

import hmac
import json
from hashlib import sha256
from pathlib import Path
from time import time

from fastapi.testclient import TestClient

import app.main as main_module
from app.main import app
from app.payments.downloads import hash_download_token
from app.payments.repository import PaymentRepository
from app.settings import Settings


client = TestClient(app)


def configure_payment_test(tmp_path: Path, monkeypatch) -> Settings:
    settings = Settings(
        storage_root=tmp_path / "exports",
        payment_db_path=tmp_path / "payments.sqlite3",
        stripe_secret_key="sk_test_vector_glyphs_safe_local_only",
        stripe_webhook_secret="whsec_phase4_test_secret",
        stripe_price_export_pack="price_test_export_pack",
        public_app_url="https://vectorglyphs.test",
        download_token_secret="phase4-download-token-secret-minimum-32-chars",
        checkout_success_url="https://vectorglyphs.test/success?session_id={CHECKOUT_SESSION_ID}",
        checkout_cancel_url="https://vectorglyphs.test/#pricing",
    )
    monkeypatch.setattr(main_module, "settings", settings)
    return settings


def stripe_signature(payload: bytes, secret: str, timestamp: int | None = None) -> str:
    timestamp = timestamp or int(time())
    signed = f"{timestamp}.".encode("utf-8") + payload
    digest = hmac.new(secret.encode("utf-8"), signed, sha256).hexdigest()
    return f"t={timestamp},v1={digest}"


def checkout_payload() -> dict:
    return {
        "seed": "phase-4-checkout",
        "count": 2,
        "style": "premium-ui",
        "complexity": "balanced",
        "stroke": "#111827",
        "background": None,
        "pngSize": 512,
        "customerEmail": "buyer@example.com",
    }


def test_settings_reject_live_stripe_keys() -> None:
    try:
        Settings(stripe_secret_key="sk_live_forbidden", stripe_webhook_secret="whsec_test")
    except ValueError as error:
        assert "live Stripe keys are not allowed" in str(error)
    else:  # pragma: no cover
        raise AssertionError("live Stripe key was accepted")


def test_payment_readiness_rejects_default_download_token_secret() -> None:
    settings = Settings(
        stripe_secret_key="sk_test_vector_glyphs_safe_local_only",
        stripe_webhook_secret="whsec_phase4_test_secret",
        stripe_price_export_pack="price_test_export_pack",
    )

    try:
        settings.validate_payment_ready()
    except ValueError as error:
        assert "DOWNLOAD_TOKEN_SECRET must be changed" in str(error)
    else:  # pragma: no cover
        raise AssertionError("default download token secret was accepted")


def test_checkout_creates_pending_order_without_unlocking_download(tmp_path: Path, monkeypatch) -> None:
    settings = configure_payment_test(tmp_path, monkeypatch)

    response = client.post("/api/checkout", json=checkout_payload())

    assert response.status_code == 200
    body = response.json()
    assert body["orderId"].startswith("ord_")
    assert body["status"] == "pending"
    assert body["checkoutSessionId"].startswith("cs_test_")
    assert body["checkoutUrl"].startswith("https://checkout.stripe.com/c/pay/cs_test_")
    assert "downloadToken" not in body

    order = PaymentRepository(settings.payment_db_path).get_order(body["orderId"])
    assert order is not None
    assert order.status == "pending"
    assert order.download_token_hash is None


def test_webhook_requires_valid_stripe_signature(tmp_path: Path, monkeypatch) -> None:
    configure_payment_test(tmp_path, monkeypatch)
    response = client.post(
        "/api/stripe/webhook",
        content=json.dumps({"type": "checkout.session.completed"}).encode("utf-8"),
        headers={"stripe-signature": "t=1,v1=bad"},
    )

    assert response.status_code == 400


def test_completed_checkout_webhook_marks_order_paid_and_creates_hashed_download_token(tmp_path: Path, monkeypatch) -> None:
    settings = configure_payment_test(tmp_path, monkeypatch)
    checkout = client.post("/api/checkout", json=checkout_payload()).json()
    event = {
        "id": "evt_phase4_paid",
        "type": "checkout.session.completed",
        "data": {
            "object": {
                "id": checkout["checkoutSessionId"],
                "payment_status": "paid",
                "metadata": {"order_id": checkout["orderId"]},
            }
        },
    }
    payload = json.dumps(event, separators=(",", ":")).encode("utf-8")

    response = client.post(
        "/api/stripe/webhook",
        content=payload,
        headers={"stripe-signature": stripe_signature(payload, settings.stripe_webhook_secret)},
    )

    assert response.status_code == 200
    body = response.json()
    assert body == {"received": True}

    order = PaymentRepository(settings.payment_db_path).get_order(checkout["orderId"])
    assert order is not None
    assert order.status == "paid"
    assert order.export_id and order.export_id.startswith("exp_")
    assert order.download_token_hash is not None
    assert order.download_token_plaintext is None
    assert order.download_token_expires_at is not None
    assert order.download_token_expires_at > int(time())


def test_download_token_serves_zip_only_for_paid_unexpired_order(tmp_path: Path, monkeypatch) -> None:
    settings = configure_payment_test(tmp_path, monkeypatch)
    checkout = client.post("/api/checkout", json=checkout_payload()).json()
    event = {
        "id": "evt_phase4_download",
        "type": "checkout.session.completed",
        "data": {
            "object": {
                "id": checkout["checkoutSessionId"],
                "payment_status": "paid",
                "metadata": {"order_id": checkout["orderId"]},
            }
        },
    }
    payload = json.dumps(event, separators=(",", ":")).encode("utf-8")
    client.post(
        "/api/stripe/webhook",
        content=payload,
        headers={"stripe-signature": stripe_signature(payload, settings.stripe_webhook_secret)},
    )
    repo = PaymentRepository(settings.payment_db_path)
    token = repo.issue_download_token(checkout["orderId"], settings=settings)

    denied = client.get("/api/download/not-a-real-token")
    allowed = client.get(f"/api/download/{token}")

    assert denied.status_code == 404
    assert allowed.status_code == 200
    assert allowed.headers["content-type"] == "application/zip"
    assert allowed.content.startswith(b"PK")

    order = repo.get_order(checkout["orderId"])
    assert order is not None
    assert order.download_token_hash == hash_download_token(token, settings.download_token_secret)
    assert token not in settings.payment_db_path.read_text(errors="ignore")
