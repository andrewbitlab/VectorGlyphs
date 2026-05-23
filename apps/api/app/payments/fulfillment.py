from __future__ import annotations

from pathlib import Path
from typing import Any

from app.payments.repository import PaymentRepository
from app.services.exports import export_glyph_bundle
from app.settings import Settings


def fulfill_paid_checkout_session(session: dict[str, Any], *, settings: Settings) -> None:
    if session.get("payment_status") != "paid":
        return
    metadata = session.get("metadata") or {}
    order_id = metadata.get("order_id")
    if not order_id:
        return
    repo = PaymentRepository(settings.payment_db_path)
    order = repo.get_order(order_id)
    if order is None:
        return
    if order.status == "paid" and order.export_zip_path and Path(order.export_zip_path).exists():
        return
    export = export_glyph_bundle(order.spec_payload(), settings=settings)
    repo.mark_paid(order.id, export_id=export.export_id, export_zip_path=export.zip_path, settings=settings)
