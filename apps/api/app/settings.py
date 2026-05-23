from __future__ import annotations

from pathlib import Path

from pydantic import BaseModel, Field, field_validator

LOCAL_DEFAULT_DOWNLOAD_TOKEN_SECRET = "local-dev-download-token-secret-change-me-before-deploy"


class Settings(BaseModel):
    storage_root: Path = Field(default_factory=lambda: Path(__file__).resolve().parents[1] / "storage" / "exports")
    export_ttl_seconds: int = 3600

    # Phase 4 payment settings. Defaults are intentionally non-secret and test/local only.
    payment_db_path: Path = Field(default_factory=lambda: Path(__file__).resolve().parents[1] / "storage" / "payments.sqlite3")
    public_app_url: str = "http://127.0.0.1:3000"
    stripe_secret_key: str | None = None
    stripe_webhook_secret: str | None = None
    stripe_price_export_pack: str | None = None
    checkout_success_url: str = "http://127.0.0.1:3000/success?session_id={CHECKOUT_SESSION_ID}"
    checkout_cancel_url: str = "http://127.0.0.1:3000/#pricing"
    export_pack_amount_cents: int = 900
    currency: str = "usd"
    download_token_secret: str = LOCAL_DEFAULT_DOWNLOAD_TOKEN_SECRET
    download_token_ttl_seconds: int = 3600

    @field_validator("stripe_secret_key")
    @classmethod
    def reject_live_stripe_secret_keys(cls, value: str | None) -> str | None:
        if value and value.startswith("sk_live_"):
            raise ValueError("live Stripe keys are not allowed in this Phase 4 local/test-mode implementation")
        return value

    def validate_payment_ready(self) -> None:
        if not self.stripe_secret_key or not self.stripe_secret_key.startswith("sk_test_"):
            raise ValueError("STRIPE_SECRET_KEY must be a Stripe test-mode key starting with sk_test_")
        if not self.stripe_webhook_secret or not self.stripe_webhook_secret.startswith("whsec_"):
            raise ValueError("STRIPE_WEBHOOK_SECRET must be configured for webhook verification")
        if not self.stripe_price_export_pack or not self.stripe_price_export_pack.startswith("price_"):
            raise ValueError("STRIPE_PRICE_EXPORT_PACK must be configured")
        if self.download_token_secret == LOCAL_DEFAULT_DOWNLOAD_TOKEN_SECRET:
            raise ValueError("DOWNLOAD_TOKEN_SECRET must be changed before enabling payments")
        if len(self.download_token_secret) < 32:
            raise ValueError("DOWNLOAD_TOKEN_SECRET must be at least 32 characters")
