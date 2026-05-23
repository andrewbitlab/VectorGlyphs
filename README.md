# VectorGlyphs

VectorGlyphs is an independent web product for generating premium circular vector glyphs and exporting production-ready SVG/PNG assets for apps, UI, dashboards, branding, landing pages, presentations, and digital products.

**Domain:** `vectorglyphs.com`

**Positioning:** Vector Glyph Generator — create SVG & PNG glyphs for apps, UI, logos, and digital products.

**MVP direction:** free previews, deterministic procedural generation, Stripe Checkout for paid exports, tokenized downloads, commercial-use license, and Docker-based deployment through a LAN host exposed by Cloudflare Tunnel.

## Current phase

Phase 4 payment-confirmed downloads are implemented in a local/test-mode-safe form:

- Phase 1 standalone `glyph_core` Python package remains available under `packages/glyph-core/python`
- Next.js + TypeScript + Tailwind app lives under `apps/web`
- FastAPI export backend lives under `apps/api`
- API endpoints for health, deterministic generation previews, and local SVG/PNG/ZIP export bundles
- local filesystem export storage under ignored runtime storage
- payment order schema, pending orders, checkout-session creation, verified webhook handling, webhook idempotency, and tokenized downloads
- paid exports are generated only after a verified `checkout.session.completed` webhook reports `payment_status=paid`
- success page explains that browser redirects do not unlock paid downloads
- tests cover payment safety, signature verification, token hashing, paid-only downloads, API generation/export, web UI, and glyph core

No live Stripe keys, deployment, cron jobs, external publishing, paid resources, or account automation have been created. The payment flow rejects live Stripe secret keys and is intended for local/test-mode validation only.

## Planned stack

- Frontend: Next.js + TypeScript + Tailwind CSS
- Backend: FastAPI + Python
- Glyph core: importable Python package under `packages/glyph-core/python`
- Storage: local Docker volume for MVP
- Database: Postgres
- Payments: Stripe Checkout + verified webhooks
- Deployment: Docker Compose on LAN host + Cloudflare Tunnel

## Repository layout

```txt
apps/web/              Next.js + TypeScript + Tailwind Web MVP
apps/api/              FastAPI local export backend
packages/glyph-core/   Standalone glyph generation package and reference material
infra/                 Future Docker/Caddy/Cloudflare deployment files
docs/                  Product, architecture, API, deployment, SEO, launch docs
scripts/               Future local maintenance/import scripts
marketing/             Future marketing outbox and performance tracking
```

See `VECTORGLYPHS_MASTER_PROMPT.md` for the source plan and `ROADMAP.md` / `BACKLOG.md` for phased execution.
