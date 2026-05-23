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

Status: complete.

Goal: create a standalone, tested Python glyph generation package.

Completed:

- Copied the original generator into this repo as reference.
- Refactored generation into `packages/glyph-core/python/glyph_core`.
- Defined generation specs and output models.
- Added deterministic generation tests.
- Added SVG validity/security tests.
- Added PNG export dimensions test.
- Generated a Phase 1 sample gallery.

## Phase 2 — Web MVP without payment

Status: complete.

Goal: a premium local web experience with live preview and SEO sections, but no payment unlock yet.

Completed:

- Scaffold Next.js + TypeScript + Tailwind.
- Build hero and embedded generator.
- Add style/color/complexity/size controls.
- Add example grid and use-case sections.
- Add FAQ, metadata, and feedback form stub.
- Add Vitest tests for preview logic, landing copy, and rendered MVP controls.
- Verify with tests, lint, production build, local production server, browser snapshot, and visual inspection.

## Phase 3 — Export backend

Status: complete.

Goal: local API support for preview/export generation.

Completed:

- Scaffold FastAPI app.
- Expose health, generation, preview/export endpoints.
- Implement SVG, PNG, and ZIP export paths.
- Add local filesystem storage layout.
- Add integration tests.
- Keep backend local-only; no Stripe/payment/deployment work.

## Phase 4 — Stripe payment

Status: complete in local/test-mode-safe form.

Goal: payment-confirmed downloads.

Completed:

- Add production-equivalent Postgres order/session DDL plus local SQLite-backed test-mode repository.
- Add server-side checkout-session creation that creates pending orders and refuses live Stripe keys.
- Add verified webhook handling and idempotency.
- Generate paid exports only after verified webhook confirmation.
- Add hashed, expiring tokenized download flow and success page.
- Test in local Stripe test-mode/signed-webhook simulation only; no live payments or deployment.

## Phase 4.5 — Premium UX & retention layer

Status: complete.

Goal: turn the technical MVP into a premium, exploratory product experience that makes users want to generate, compare, and use glyphs inside real interfaces.

Completed:

- Upgrade the landing page from functional MVP to dark, megapremium design-tool presentation.
- Reframe the generator as a live premium glyph studio with stronger visual hierarchy and retention copy.
- Add retention mechanics: variation loop, keeper-set framing, recently generated state, contextual preview nudges, and export confidence messaging.
- Add product-context mockups for onboarding screens, dashboard cards, and brand system tiles.
- Expand browser generator variety with segmented outer rings, filled line systems, and 50 distinct review-board structures.
- Add `/glyph-lab` numbered feedback board for iterative visual curation.
- Update web tests to enforce premium/retention content and product-context sections.

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
