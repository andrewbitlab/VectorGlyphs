# API Design — VectorGlyphs

No API has been implemented in Phase 0. This document captures the planned contracts.

## Planned routes

### `POST /api/generate`

Generate a temporary preview job from a seed/spec.

### `GET /api/preview/:jobId/:glyphId.png`

Return a small preview image for a generated glyph.

### `POST /api/checkout`

Create a server-priced Stripe Checkout Session for a selected export.

### `POST /api/stripe/webhook`

Verify Stripe signature and process payment events idempotently.

### `GET /api/order/:orderId`

Return order/export readiness status.

### `GET /api/download/:token`

Serve tokenized paid download attachment.

### `POST /api/feedback`

Accept optional email/use-case/rating feedback and forward to Telegram when configured.

## Validation requirements

- Whitelist styles, complexities, PNG sizes, formats, and color formats.
- Limit generation count.
- Never trust client-provided price.
- Rate-limit generate, checkout, download, and feedback endpoints.
