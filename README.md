# VectorGlyphs

VectorGlyphs is an independent web product for generating premium circular vector glyphs and exporting production-ready SVG/PNG assets for apps, UI, dashboards, branding, landing pages, presentations, and digital products.

**Domain:** `vectorglyphs.com`

**Positioning:** Vector Glyph Generator — create SVG & PNG glyphs for apps, UI, logos, and digital products.

**MVP direction:** free previews, deterministic procedural generation, Stripe Checkout for paid exports, tokenized downloads, commercial-use license, and Docker-based deployment through a LAN host exposed by Cloudflare Tunnel.

## Current phase

Phase 2 web MVP without payment is complete locally:

- Phase 1 standalone `glyph_core` Python package remains available under `packages/glyph-core/python`
- Next.js + TypeScript + Tailwind app lives under `apps/web`
- premium landing page with hero, examples, use cases, exports, license, pricing hypothesis, FAQ, and feedback stub
- client-side deterministic preview generator with seed/style/complexity/color/background/format/PNG-size controls
- SEO metadata for `vectorglyphs.com`
- Vitest component/unit tests, ESLint, and production build verification

No payment integration, export backend, deployment, cron jobs, external publishing, paid resources, or account automation have been created yet.

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
apps/api/              Future FastAPI export backend
packages/glyph-core/   Standalone glyph generation package and reference material
infra/                 Future Docker/Caddy/Cloudflare deployment files
docs/                  Product, architecture, API, deployment, SEO, launch docs
scripts/               Future local maintenance/import scripts
marketing/             Future marketing outbox and performance tracking
```

See `VECTORGLYPHS_MASTER_PROMPT.md` for the source plan and `ROADMAP.md` / `BACKLOG.md` for phased execution.
