# Stripe Plan — VectorGlyphs

Stripe is not configured or called in Phase 0.

## Checkout strategy

Use Stripe Checkout first. Do not build custom card forms for the MVP.

## Required behavior

- Server determines product/price.
- Create a pending order before creating Checkout Session.
- Store Stripe session/payment metadata.
- Verify webhook signatures.
- Process events idempotently.
- Generate paid exports only after webhook-confirmed payment.
- Never unlock downloads solely from success-page redirects.

## Planned metadata

```json
{
  "orderId": "ord_123",
  "jobId": "job_abc123",
  "glyphId": "glyph_001",
  "exportSpecHash": "sha256..."
}
```

## Planned events

- `checkout.session.completed`
- `payment_intent.succeeded`
- `payment_intent.payment_failed`
- `charge.refunded` later
