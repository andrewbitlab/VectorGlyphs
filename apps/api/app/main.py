from __future__ import annotations

from fastapi import FastAPI, Header, HTTPException, Request
from fastapi.responses import FileResponse

from app.payments.checkout import create_checkout_session
from app.payments.fulfillment import fulfill_paid_checkout_session
from app.payments.repository import PaymentRepository
from app.payments.webhooks import WebhookSignatureError, verify_stripe_webhook
from app.schemas import (
    CheckoutRequest,
    CheckoutResponse,
    ExportRequest,
    ExportResponse,
    GenerateRequest,
    GenerateResponse,
)
from app.services.exports import export_glyph_bundle
from app.services.glyphs import generate_preview_response
from app.settings import Settings

app = FastAPI(title="VectorGlyphs API", version="0.1.0")
settings = Settings()


@app.get("/health")
def health() -> dict[str, bool | str]:
    return {"ok": True, "service": "vectorglyphs-api", "version": "0.1.0"}


@app.post("/api/generate", response_model=GenerateResponse, response_model_by_alias=True)
def generate(request: GenerateRequest) -> GenerateResponse:
    return generate_preview_response(request)


@app.post("/api/export", response_model=ExportResponse, response_model_by_alias=True)
def export(request: ExportRequest) -> ExportResponse:
    result = export_glyph_bundle(request, settings=settings)
    return ExportResponse(
        exportId=result.export_id,
        fileCount=len(result.svg_paths) + len(result.png_paths) + 2,
        zipFile=result.zip_path.name,
        manifestFile=result.manifest_path.name,
        storagePath=str(result.storage_path),
        expiresInSeconds=settings.export_ttl_seconds,
    )


@app.post("/api/checkout", response_model=CheckoutResponse, response_model_by_alias=True)
def checkout(request: CheckoutRequest) -> CheckoutResponse:
    try:
        result = create_checkout_session(request.model_dump(by_alias=True), settings=settings)
    except ValueError as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc
    return CheckoutResponse(
        orderId=result.order.id,
        checkoutSessionId=result.checkout_session_id,
        checkoutUrl=result.checkout_url,
    )


@app.post("/api/stripe/webhook")
async def stripe_webhook(request: Request, stripe_signature: str = Header(default="")) -> dict[str, bool]:
    payload = await request.body()
    try:
        event = verify_stripe_webhook(payload, stripe_signature, settings.stripe_webhook_secret or "")
    except (WebhookSignatureError, ValueError) as exc:
        raise HTTPException(status_code=400, detail="invalid Stripe webhook signature") from exc

    event_id = str(event.get("id", ""))
    event_type = str(event.get("type", ""))
    repo = PaymentRepository(settings.payment_db_path)
    if event_id and not repo.record_webhook_once(event_id, event_type):
        return {"received": True}

    if event_type == "checkout.session.completed":
        session = event.get("data", {}).get("object", {})
        if isinstance(session, dict):
            fulfill_paid_checkout_session(session, settings=settings)
    return {"received": True}


@app.get("/api/download/{token}")
def download(token: str) -> FileResponse:
    order = PaymentRepository(settings.payment_db_path).get_paid_order_by_download_token(token, settings=settings)
    if order is None or order.export_zip_path is None:
        raise HTTPException(status_code=404, detail="download not found")
    return FileResponse(order.export_zip_path, media_type="application/zip", filename=f"{order.export_id}.zip")
