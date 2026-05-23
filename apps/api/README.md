# VectorGlyphs API

Phase 4 implements the local FastAPI export/payment backend for glyph generation, file exports, and payment-confirmed downloads.

## Implemented endpoints

- `GET /health` — service health and version.
- `POST /api/generate` — deterministic glyph preview response with inline SVG.
- `POST /api/export` — local export bundle generation with SVG files, PNG files, `manifest.json`, and a ZIP archive.
- `POST /api/checkout` — creates a pending order and Stripe test-mode checkout session metadata.
- `POST /api/stripe/webhook` — verifies Stripe webhook signatures, handles idempotency, and fulfills paid orders.
- `GET /api/download/{token}` — serves the paid ZIP only when the token is valid, hashed server-side, and unexpired.

## Payment safety rules

- Live Stripe secret keys are rejected by settings validation.
- Browser redirects never unlock files; only a verified webhook can mark an order paid.
- Download tokens are random, short-lived, and stored only as HMAC-SHA256 hashes.
- Runtime exports, SQLite payment DBs, virtualenvs, and caches are ignored by git.
- The local Phase 4 repository uses SQLite for safe test-mode development. `db/migrations/001_payment_orders.sql` documents the production-equivalent Postgres schema for later Docker/Postgres work.

## Local commands

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -e '.[dev]' -e ../../packages/glyph-core/python
.venv/bin/python -m pytest -q
.venv/bin/uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

Export and payment artifacts are written under local ignored storage. Phase 4 payment artifacts are local/test-mode only and do not deploy, charge real cards, or require committed secrets.
