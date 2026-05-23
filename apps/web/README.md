# VectorGlyphs Web MVP

Phase 2 implements the local web MVP without payment, deployment, cron jobs, or external service integrations.

## Stack

- Next.js App Router
- TypeScript
- Tailwind CSS
- Vitest + Testing Library
- ESLint

## Implemented

- SEO metadata for the Vector Glyph Generator positioning.
- Premium dark landing page with hero, examples, use cases, export explanation, license copy, pricing hypothesis, FAQ, and feedback stub.
- Client-side deterministic preview generator with controls for seed, style, complexity, stroke color, background, export format, and PNG size.
- Clear Phase 2 no-payment messaging: Stripe checkout is deferred to Phase 4.

## Local commands

```bash
npm install
npm test
npm run lint
npm run build
npm run start -- --hostname 127.0.0.1 --port 3000
```

The preview generator in this phase is browser-local. Phase 3 will replace/augment it with the FastAPI export backend and the Python `glyph_core` package.
