# Marketing Automation — VectorGlyphs

No marketing automation or cron jobs are active in Phase 0.

## Future skill concept

Create a reusable `vectorglyphs-visual-marketing` workflow that can:

- generate glyph-based UI inspiration visuals
- render deterministic HTML/CSS/SVG mockups with Playwright
- write captions, alt text, and metadata
- save assets to `marketing/outbox`
- publish only to explicitly approved platforms with configured credentials and safe automation paths
- track URLs/performance and learn from results

## Autonomy guardrails

- Prefer official APIs or platform-supported schedulers.
- Use Surfagent/browser automation only for permitted ordinary UI flows.
- Stop for CAPTCHA, 2FA, security challenges, or ToS uncertainty.
- Avoid spammy frequency.
- Keep quality high.
- Do not publish without a configured approval policy.
