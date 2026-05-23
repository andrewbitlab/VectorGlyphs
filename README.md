# VectorGlyphs

VectorGlyphs is an independent web product for generating premium circular vector glyphs and exporting production-ready SVG/PNG assets for apps, UI, dashboards, branding, landing pages, presentations, and digital products.

**Domain:** `vectorglyphs.com`

**Positioning:** Vector Glyph Generator — create SVG & PNG glyphs for apps, UI, logos, and digital products.

**MVP direction:** free previews, deterministic procedural generation, Stripe Checkout for paid exports, tokenized downloads, commercial-use license, and Docker-based deployment through a LAN host exposed by Cloudflare Tunnel.

## Current phase

Phase 1 glyph core is complete:

- original generator copied as in-repo reference
- standalone `glyph_core` Python package
- deterministic seed/spec generation
- clean SVG rendering
- PNG export helper
- manifest builder
- pytest coverage
- sample gallery under `packages/glyph-core/sample-gallery/phase1`

No web app, payment integration, deployment, cron jobs, or external publishing have been created yet.

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
apps/                  Future web and API apps
packages/glyph-core/   Future standalone glyph generation package
infra/                 Future Docker/Caddy/Cloudflare deployment files
docs/                  Product, architecture, API, deployment, SEO, launch docs
scripts/               Future local maintenance/import scripts
marketing/             Future marketing outbox and performance tracking
```

See `VECTORGLYPHS_MASTER_PROMPT.md` for the source plan and `ROADMAP.md` / `BACKLOG.md` for phased execution.
