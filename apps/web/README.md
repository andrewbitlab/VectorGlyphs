# VectorGlyphs Web

Phase 4.5 upgrades the local web experience from a functional MVP into a premium, retention-oriented product surface. It still does not deploy, create cron jobs, or use external marketing automation.

## Stack

- Next.js App Router
- TypeScript
- Tailwind CSS
- Vitest + Testing Library
- ESLint

## Implemented

- SEO metadata for the Vector Glyph Generator positioning.
- Megapremium dark landing page with hero, examples, use cases, export explanation, license copy, pricing hypothesis, FAQ, and feedback stub.
- Client-side deterministic preview generator presented as a live premium glyph studio with controls for seed, style, complexity, stroke color, background, export format, and PNG size.
- Retention layer: variation loop, keeper-set framing, recently generated state, product-context previews, and export-confidence messaging.
- Glyph-in-context mockups for app onboarding, dashboard cards, and brand system tiles.
- Expanded browser generator with 50 distinct review-board structures, segmented/broken outer rings, filled line systems, geometric cores, orbit dots, and organic variants.
- `/glyph-lab` numbered 50-glyph feedback board for selecting weak designs by number before the next iteration.
- Payment-safe messaging: redirects do not unlock paid files; webhook-confirmed exports and tokenized downloads are handled by the API.

## Local commands

```bash
npm install
npm test
npm run lint
npm run build
npm run start -- --hostname 127.0.0.1 --port 3000
```

The preview generator remains browser-local for instant exploration. The FastAPI backend and Python `glyph_core` package provide server-side generation/export/payment-confirmed download paths.
