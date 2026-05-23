# Deployment Plan — VectorGlyphs

Deployment is not active in Phase 0. This document records the intended path only.

## Target architecture

- Next.js frontend/BFF.
- FastAPI internal backend.
- Postgres for orders/payment state/generation metadata.
- Local Docker volume for generated previews and paid export files.
- Optional Redis later for rate limits, locks, or short-lived job cache.
- Caddy or Traefik reverse proxy.
- Cloudflare Tunnel exposing the LAN host to `vectorglyphs.com`.

## Production rule

Do not deploy, create paid resources, change DNS, register services, or expose public endpoints without explicit user approval.

## Planned Docker services

- `web` — Next.js app.
- `api` — FastAPI app, internal network only.
- `postgres` — order/session/payment metadata.
- `proxy` — Caddy/Traefik if needed.
- `cloudflared` — only after Cloudflare Tunnel is approved/configured.

## Storage layout

Planned local volume:

```txt
/data/vector-glyphs/
  jobs/
    <hash-prefix>/
      <job-id>/
        spec.json
        manifest.json
        previews/
        svg/
        exports/
```

TTL policy:

- Unpaid generation jobs: 24h.
- Paid exports: 30 days initially.
- Order/payment records: retain for accounting/legal needs.

## Required future environment variables

See `.env.example` for the complete starting list.

## Verification commands later

```bash
# Python tests
cd apps/api && python -m pytest -q

# Glyph core tests
cd packages/glyph-core/python && python -m pytest -q

# Web tests/lint
cd apps/web && npm run lint && npm run test

# Build
cd apps/web && npm run build

# Docker
cd infra && docker compose up -d --build

# Health
curl -fsS http://localhost:3000/api/health
curl -fsS http://localhost:8000/internal/health
```

These commands are placeholders until the corresponding apps are scaffolded.
