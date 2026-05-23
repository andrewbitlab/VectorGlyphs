# Architecture — VectorGlyphs

## Planned system

```txt
Browser
  ↓
Next.js web app / BFF
  ↓ internal network
FastAPI glyph/export API
  ↓
glyph_core package + filesystem storage + Postgres
```

## Components

- `apps/web`: future Next.js + TypeScript + Tailwind app.
- `apps/api`: future FastAPI app for generation/export/payment-adjacent internal operations.
- `packages/glyph-core/python`: future standalone Python package for deterministic glyph generation, SVG rendering, manifests, and PNG export helpers.
- `infra`: future Docker Compose, reverse proxy, and Cloudflare Tunnel configuration.

## Core principles

- Deterministic generation by seed/spec.
- Clean SVG with no scripts or external resources.
- Server-side paid export generation.
- Stripe webhook as source of truth.
- Tokenized downloads with TTL.
- No user accounts for MVP.
- Keep the first architecture boring and maintainable.
