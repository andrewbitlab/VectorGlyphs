# Roadmap — VectorGlyphs

## Phase 0 — Project foundation

Status: complete after this foundation commit.

Scope:

- Repository skeleton.
- Core docs.
- `.gitignore` and `.env.example`.
- Strict `AGENTS.md` boundaries.
- No web app implementation, deployment, paid resources, or cron jobs.

## Phase 1 — Extract glyph core

Goal: create a standalone, tested Python glyph generation package.

Tasks:

- Copy the original generator into this repo as reference only after verifying the expected source path.
- Refactor into `packages/glyph-core/python/glyph_core`.
- Define generation specs and output models.
- Add deterministic generation tests.
- Add SVG validity/security tests.
- Add sample gallery generation script.
- Confirm representative glyph snapshots.

## Phase 2 — Web MVP without payment

Goal: a premium local web experience with live preview and SEO sections, but no payment unlock yet.

Tasks:

- Scaffold Next.js + TypeScript + Tailwind.
- Build hero and embedded generator.
- Add style/color/complexity/size controls.
- Add example grid and use-case sections.
- Add FAQ, metadata, and feedback form stub.

## Phase 3 — Export backend

Goal: local API support for preview/export generation.

Tasks:

- Scaffold FastAPI app.
- Expose health, generation, preview/export endpoints.
- Implement SVG, PNG, and ZIP export paths.
- Add local filesystem storage layout.
- Add integration tests.

## Phase 4 — Stripe payment

Goal: payment-confirmed downloads.

Tasks:

- Add Postgres order/session schema.
- Add server-side Stripe Checkout creation.
- Add verified webhook handling and idempotency.
- Generate paid exports only after webhook confirmation.
- Add tokenized download flow and success page.
- Test in Stripe test mode only.

## Phase 5 — Docker deployment

Goal: production-ready deployment configuration, with deployment only after user approval.

Tasks:

- Create Dockerfiles and Compose files.
- Add Caddy/Traefik configuration.
- Add Cloudflare Tunnel example config.
- Verify local Docker runtime.
- Document LAN host deployment steps.

## Phase 6 — SEO and launch

Goal: prepare public launch assets and search footprint.

Tasks:

- Add sitemap and robots.
- Draft programmatic SEO pages.
- Prepare launch copy for Product Hunt, HN, Reddit, X, and directories.
- Add analytics plan/dashboard.

## Phase 7 — Autonomous visual marketing

Goal: create a safe, high-quality visual marketing pipeline.

Tasks:

- Create `vectorglyphs-visual-marketing` skill/spec.
- Generate HTML/CSS/SVG UI mockups using VectorGlyphs glyphs.
- Render images with Playwright.
- Save outbox assets and metadata.
- Add quality gate.
- Build platform adapters only where safe/API-supported.
- Create marketing cron only after user approval.
