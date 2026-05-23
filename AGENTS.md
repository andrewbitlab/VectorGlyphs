# VectorGlyphs Agent Operating Rules

This repository is the independent VectorGlyphs project. It must stay separate from all other repositories and products.

## Hard boundaries

- Work only inside this repository unless the user explicitly approves a specific external read/copy action.
- Do not modify PowerAppMVP2, AppStoreMillion, or any other repository.
- Do not create cross-repository imports, symlinks, shared mutable dependencies, or runtime coupling to other projects.
- If reference code from another project is useful, copy only the necessary files into this repository and refactor them here.
- Do not read or use secrets from unrelated projects.
- Do not commit `.env`, API keys, tokens, account cookies, Stripe secrets, Cloudflare credentials, Telegram bot tokens, or other secrets.
- Do not register domains, create paid resources, publish public content, send outreach, deploy to production, or spend money without explicit user approval.
- Do not create cron jobs until the user explicitly approves the exact job prompts and schedules.
- Browser automation for marketing/publishing may only use ordinary permitted platform UI flows and must stop for CAPTCHA, 2FA, security challenges, or ToS uncertainty.

## Product intent

VectorGlyphs should become a premium procedural vector design tool, not a generic AI-art toy.

Core promise:

> Create unique circular SVG and PNG glyphs in seconds. Perfect for app interfaces, websites, branding, dashboards, empty states, onboarding screens, and digital products.

## Technical guardrails

- Keep generated SVG deterministic, clean, script-free, and commercially usable.
- Validate all external input with Zod/Pydantic once implementation begins.
- Stripe webhooks are the payment source of truth; never unlock paid downloads from browser redirects alone.
- Download links must use random tokenized URLs with hashed tokens and TTLs.
- Keep FastAPI internal behind the Next.js BFF unless architecture changes are documented.
- Prefer local prototypes, docs, and tests before deployment.

## Phase discipline

Proceed phase-by-phase from `VECTORGLYPHS_MASTER_PROMPT.md`:

1. Phase 0: foundation/docs/skeleton only.
2. Phase 1: import/refactor glyph core with tests.
3. Phase 2: web MVP without payment.
4. Phase 3: export backend.
5. Phase 4: Stripe payment.
6. Phase 5: Docker deployment.
7. Phase 6: SEO and launch.
8. Phase 7: autonomous visual marketing.

Do not jump ahead without user approval.

## Verification habit

Before reporting success, verify filesystem changes, git status, and any relevant tests/linters for the current phase. For Phase 0, verification means confirming structure and documentation exist and that no app implementation/deployment/cron actions were performed.
