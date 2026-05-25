# Backlog — VectorGlyphs

## Foundation

- [x] Create project skeleton.
- [x] Add AGENTS.md with project boundaries.
- [x] Add product brief.
- [x] Add business plan.
- [x] Add roadmap.
- [x] Add deployment plan.
- [x] Add marketing plan.
- [x] Add .env.example.

## Generator

- [x] Verify source path for original generator candidate.
- [x] Import original generator as reference inside this repository.
- [x] Refactor generator into `glyph_core`.
- [x] Add seed-based generation.
- [x] Add palette controls.
- [x] Add complexity controls.
- [x] Add SVG validation tests.
- [x] Add PNG export tests.
- [x] Add representative output tests.
- [x] Generate sample gallery.

## Vectorizer.app pivot

- [x] Add first `packages/vectorizer-core/python` package.
- [x] Add monochrome foreground extraction for light and dark source sheets.
- [x] Add icon-sheet segmentation into numbered glyph crops.
- [x] Add fidelity-first SVG export without embedded rasters/scripts/external resources.
- [x] Add SVG-to-PNG roundtrip comparison, diffs, manifest, and contact sheet reports.
- [x] Validate first 152-glyph benchmark with visually perfect normalized-crop roundtrip.
- [x] Add quality-gated `potrace`/`vtracer` tracing with exact fallback.
- [x] Add batch export into one pack directory per source image.
- [x] Add final product PNG export at 500×500 per glyph.
- [x] Validate current local batch: 33 readable packs, 3,745 PNGs, no missing artifacts, no bad PNG sizes.
- [ ] Add automated curation filters for text fragments, watermarks, clipped symbols, and low-value noisy detections.
- [ ] Add cleaner primitive optimizer that only replaces fidelity paths when diff remains human-invisible.
- [ ] Add interactive vectorizer review lab UI.
- [ ] Add manual split/merge correction controls for difficult source sheets.
- [ ] Add pack builder for curated VectorGlyphs products.

## Web

- [x] Scaffold Next.js app.
- [x] Build hero section.
- [x] Build live generator UI.
- [x] Build examples grid.
- [x] Build use-case sections.
- [x] Build FAQ.
- [x] Build feedback form.
- [x] Add SEO metadata.
- [x] Add web tests, lint config, and production build verification.
- [x] Add Phase 4.5 premium UX/retention redesign.
- [x] Add glyph-in-context mockups for onboarding, dashboards, and brand tiles.
- [x] Add retention copy for variation exploration, keeper sets, contextual preview, and confident export.
- [x] Expand browser generator variety to 50 distinct review-board structures.
- [x] Add segmented/broken outer ring and filled line-system glyph families.
- [x] Add `/glyph-lab` numbered visual feedback board.

## API / exports

- [x] Scaffold FastAPI app.
- [x] Add health endpoint.
- [x] Add generation endpoint.
- [x] Add preview endpoint.
- [x] Add export endpoint.
- [x] Implement PNG export.
- [x] Implement ZIP export.
- [x] Add local storage layout.
- [x] Add integration tests.

## Payments

- [x] Add Postgres schema for orders.
- [x] Add Stripe Checkout session creation.
- [x] Add Stripe webhook signature verification.
- [x] Add Stripe event idempotency.
- [x] Add tokenized download.
- [x] Add success page.
- [x] Test in Stripe test mode.

## Deployment

- [ ] Add Docker Compose.
- [ ] Add production compose.
- [ ] Add Caddy/Traefik config.
- [ ] Add Cloudflare Tunnel instructions.
- [ ] Add health endpoint checks.
- [ ] Deploy to LAN host after user approval.

## Marketing

- [ ] Create SEO keyword list.
- [ ] Draft first 10 SEO pages.
- [ ] Draft Product Hunt copy.
- [ ] Draft HN Show HN post.
- [ ] Draft X launch thread.
- [ ] Design first 10 UI inspiration image concepts.
- [ ] Create visual marketing skill spec.
- [ ] Research platform posting/API feasibility.
- [ ] Create marketing outbox schema.
