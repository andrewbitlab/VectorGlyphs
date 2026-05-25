# VectorGlyphs

VectorGlyphs is an independent web product for creating and selling premium vector glyph packs for apps, UI, dashboards, branding, landing pages, presentations, and digital products.

**Domain:** `vectorglyphs.com`

**Positioning:** Vector Glyph Generator — create SVG & PNG glyphs for apps, UI, logos, and digital products.

**Pivot direction:** sell curated ready-made glyph packs, powered by an internal `vectorizer.app` workflow that extracts monochrome icon sheets into individual high-fidelity SVG files. The earlier procedural generator remains useful for experimentation, review boards, and future pack creation.

## Current phase

Phase 4.5 premium UX and retention redesign is complete on top of the local/test-mode-safe payment flow:

- Phase 1 standalone `glyph_core` Python package remains available under `packages/glyph-core/python`
- Next.js + TypeScript + Tailwind app lives under `apps/web`
- FastAPI export backend lives under `apps/api`
- API endpoints for health, deterministic generation previews, and local SVG/PNG/ZIP export bundles
- local filesystem export storage under ignored runtime storage
- payment order schema, pending orders, checkout-session creation, verified webhook handling, webhook idempotency, and tokenized downloads
- paid exports are generated only after a verified `checkout.session.completed` webhook reports `payment_status=paid`
- success page explains that browser redirects do not unlock paid downloads
- upgraded web experience frames VectorGlyphs as a premium design tool, not a generic AI-art toy
- retention-focused studio experience encourages users to generate variations, build keeper sets, preview glyphs in real UI contexts, and export with confidence
- browser preview generator now includes a wider set of symmetric glyph structures, including segmented outer rings and filled line systems
- `/glyph-lab` provides a 50-glyph numbered feedback board for fast visual iteration
- `packages/vectorizer-core/python` now performs monochrome icon-sheet segmentation, quality-gated `potrace`/`vtracer`/fallback SVG vectorization, rendered-PNG comparison, diff artifacts, per-pack manifests, contact sheets, and final PNG export at 500×500
- tests cover payment safety, signature verification, token hashing, paid-only downloads, API generation/export, premium web UI, vectorizer core, and glyph core

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
packages/vectorizer-core/ Monochrome icon-sheet extraction and SVG vectorization engine
infra/                 Future Docker/Caddy/Cloudflare deployment files
docs/                  Product, architecture, API, deployment, SEO, launch docs
scripts/               Future local maintenance/import scripts
marketing/             Future marketing outbox and performance tracking
```

See `VECTORGLYPHS_MASTER_PROMPT.md` for the original source plan, `docs/vectorizer-app-pivot.md` for the pivot, and `ROADMAP.md` / `BACKLOG.md` for phased execution.
