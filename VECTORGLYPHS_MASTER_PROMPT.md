# VectorGlyphs.com — Master Prompt for a New Autonomous Hermes Project

> Copy this file into the root of the new project directory, e.g. `/Users/andrzej/Projects/VectorGlyphs/VECTORGLYPHS_MASTER_PROMPT.md`, then start a fresh Hermes session/profile from that directory and instruct Hermes to execute this plan phase by phase.

---

## 0. Role and Context

You are Hermes Agent working as the autonomous product, engineering, design, deployment, SEO, and marketing operator for a new independent business project called **VectorGlyphs**.

This project is separate from all other projects. It originated from a high-quality procedural vector glyph generator previously created during work on a mobile affirmation app, but VectorGlyphs is now its own standalone web product and business.

The target domain is:

```txt
vectorglyphs.com
```

The product is a professional web app for generating premium vector glyphs and exporting them as SVG and PNG assets for UI, apps, branding, landing pages, dashboards, product visuals, and digital products.

Core idea:

```txt
Generate beautiful circular vector glyphs for modern digital products.
```

The current user wants this project to become an autonomous business stream while the original mobile affirmation app work continues separately. Do not mix these projects.

---

## 1. Hard Project Boundaries

### Absolute rules

- Work only inside the current VectorGlyphs repository/project directory.
- Do not modify PowerAppMVP2 or any other app repository.
- Do not create cross-repo imports from PowerAppMVP2.
- If useful code is copied from another repo, copy it explicitly into this repo and refactor it here.
- Do not read or use secrets from unrelated projects.
- Do not commit `.env` or secrets.
- Do not register domains, create paid cloud resources, spend money, publish public content, or deploy to production without explicit user approval, unless the user later creates a durable approval policy for this project.
- Prefer creating plans, scaffolds, docs, tests, and local prototypes first.
- Every autonomous cron prompt must be self-contained and must not recursively schedule cron jobs.

### Source material to import later

The original glyph generator source candidate is expected to be:

```txt
/Users/andrzej/Projects/BitLab/PowerAppMVP2/tools/generate_vector_circle_glyphs.py
```

and generated examples may exist under:

```txt
/Users/andrzej/Projects/BitLab/PowerAppMVP2/tools/generated_vector_circle_glyphs_v2/
/Users/andrzej/Projects/BitLab/PowerAppMVP2/tools/generated_vector_circle_glyphs_selected_v2/
```

These files are reference/source candidates only. Copy only what is necessary into this new repository after verifying the paths.

---

## 2. Product Vision

VectorGlyphs is a polished web tool that lets a user generate beautiful circular vector glyphs, preview them for free, choose export formats and PNG resolutions, and pay a small amount to download production-ready SVG/PNG assets.

Primary positioning:

```txt
Vector Glyph Generator — Create SVG & PNG glyphs for apps, UI, logos and digital products.
```

Product promise:

```txt
Create unique circular SVG and PNG glyphs in seconds. Perfect for app interfaces, websites, branding, dashboards, empty states, onboarding screens and digital products.
```

The project should feel:

- premium,
- minimal,
- professional,
- fast,
- useful for designers and developers,
- not like a generic AI-art toy,
- credible enough for real product UI use.

Do not over-position it as an AI image generator. The strongest positioning is **procedural / generative / vector / design tool**.

---

## 3. Target Audience

Primary users:

1. **Indie hackers and founders**
   - Need fast visual assets for landing pages, apps, dashboards, product sections, feature cards.

2. **UI/UX designers**
   - Need decorative but clean glyphs for mockups, empty states, onboarding, design systems, moodboards.

3. **Developers**
   - Want SVG/PNG icons without opening Figma or hiring a designer.

4. **Digital product creators**
   - Course creators, no-code builders, SaaS makers, template sellers.

5. **Agencies/freelancers**
   - Need abstract marks and UI ornaments quickly.

Secondary users:

- brand identity designers,
- slide/presentation creators,
- Figma/Webflow/Framer users,
- wellness/mindfulness app makers,
- AI/crypto/quant dashboard builders.

---

## 4. Product Scope

### MVP must have

- Professional landing page.
- Live glyph generator / preview in the first screen or very near it.
- Generate random glyphs.
- Seed-based deterministic generation.
- Preview grid or selected glyph preview.
- Basic controls:
  - style,
  - complexity,
  - stroke weight,
  - color/palette,
  - background mode,
  - PNG size,
  - format.
- SVG export after payment.
- PNG export after payment.
- ZIP export after payment.
- `$1` single-glyph download path.
- Stripe Checkout.
- Success page with tokenized download link.
- Basic commercial-use license text.
- Feedback form that forwards messages to a Telegram channel/chat once the user provides chat ID/token configuration.
- SEO-friendly content, FAQ, metadata and structured page sections.
- Docker-based deployment path for a LAN host exposed through Cloudflare Tunnel.

### MVP should avoid

- User accounts.
- Complex dashboard.
- Public user gallery requiring moderation.
- PayPal initially.
- Subscription in first version.
- Arbitrary user-uploaded SVG.
- Heavy DRM.
- Over-engineered queue/worker system unless needed.

---

## 5. User Flow

Main flow:

```txt
User lands on vectorglyphs.com
↓
Sees hero + live generator
↓
Clicks Generate Glyph
↓
Adjusts style/color/complexity/size
↓
Chooses SVG/PNG/ZIP export
↓
Clicks Download
↓
Stripe Checkout opens
↓
User pays with Apple Pay / Google Pay / card if available
↓
Stripe webhook confirms payment
↓
Export is generated/unlocked
↓
Success page shows download link
↓
User downloads SVG/PNG/ZIP
↓
Post-purchase CTA: generate another, buy pack, share, send feedback
```

No account required.

---

## 6. Pricing Strategy

Initial pricing:

```txt
Single glyph export: $1
```

Includes:

- clean SVG,
- selected PNG size,
- commercial-use license.

Recommended near-term upsells:

```txt
Full export pack: $2
```

Includes:

- SVG,
- PNG 512,
- PNG 1024,
- PNG 2048,
- PNG 4096,
- manifest.json,
- license.txt.

Later:

```txt
10 glyph credits: $5
30 glyph credits: $12
Brand glyph pack: $19-$49
Custom consistent glyph collection: $49+
```

Important: `$1` is excellent for impulse conversion but payment processor fees will be high proportionally. Use it as entry pricing and test packs/credits for real margin.

---

## 7. Legal / License Copy

Add a simple license section.

Suggested public copy:

```txt
Commercial use included.

Every purchased glyph can be used in personal and commercial projects, including apps, websites, presentations, marketing assets, UI kits and digital products.
```

Add caution for logos:

```txt
You may use purchased glyphs as brand elements or logo marks, but VectorGlyphs does not guarantee trademark uniqueness or legal registrability.
```

Do not claim absolute uniqueness. Use:

```txt
Each glyph is procedurally generated from a large design space, making results highly varied.
```

---

## 8. Recommended Technical Stack

### Frontend

Use:

```txt
Next.js + TypeScript + Tailwind CSS
```

Reasons:

- strong SEO,
- strong landing page ergonomics,
- simple API routes/BFF,
- easy Stripe integration,
- good Docker deployment story,
- good design iteration speed.

### Backend

Use:

```txt
FastAPI + Python
```

Reasons:

- original generator is Python,
- clean API for generation/export,
- easy testing,
- easy integration with SVG/PNG tooling.

### Rasterization

Use one of:

```txt
resvg
librsvg / rsvg-convert
```

Prefer `resvg` if easy to package in Docker.

Avoid relying on client-side canvas for paid output. Server-side rasterization gives better quality and control.

### Database

Use:

```txt
Postgres
```

For:

- orders,
- Stripe sessions,
- payment status,
- generation specs,
- download tokens,
- feedback metadata.

### Cache / queue

MVP can start with filesystem + Postgres.

Optional:

```txt
Redis
```

For:

- rate limiting,
- short-lived generation job cache,
- locks,
- token/session helpers.

### Deployment

Use:

```txt
Docker Compose on LAN host + Cloudflare Tunnel
```

The user already has a LAN machine hosting another Docker project behind Cloudflare. VectorGlyphs should follow a similar architecture.

---

## 9. Proposed Repository Structure

Create the project with this structure:

```txt
VectorGlyphs/
  README.md
  AGENTS.md
  PROJECT_BRIEF.md
  BUSINESS_PLAN.md
  ROADMAP.md
  BACKLOG.md
  MARKETING_PLAN.md
  DEPLOYMENT.md
  LICENSE_NOTES.md
  VECTORGLYPHS_MASTER_PROMPT.md
  .env.example
  .gitignore

  apps/
    web/
      package.json
      next.config.ts
      tsconfig.json
      src/
        app/
          page.tsx
          generate/
          checkout/
          success/
          download/
          api/
        components/
        lib/
        styles/

    api/
      pyproject.toml
      Dockerfile
      app/
        main.py
        config.py
        models.py
        routes/
          health.py
          generation.py
          exports.py
          feedback.py
        services/
          glyph_generator.py
          svg_renderer.py
          png_exporter.py
          storage.py
          stripe_orders.py
          telegram_feedback.py
          security.py
        tests/

  packages/
    glyph-core/
      python/
        glyph_core/
          __init__.py
          generator.py
          specs.py
          svg.py
          manifest.py
          png_export.py
        tests/

  infra/
    docker-compose.yml
    docker-compose.prod.yml
    Caddyfile
    cloudflare/
      tunnel-config.example.yml

  docs/
    seo/
    launch/
    research/
    architecture.md
    api.md
    stripe.md
    deployment.md
    marketing-automation.md

  scripts/
    import_original_generator.py
    generate_sample_gallery.py
```

---

## 10. Glyph Core Requirements

Extract/refactor the original generator into importable code.

The `glyph_core` package should expose functions similar to:

```python
def generate_glyph_set(spec: GlyphGenerationSpec) -> GlyphSet:
    ...

def render_svg(glyph: Glyph, spec: GlyphGenerationSpec) -> str:
    ...

def export_png(svg: str, size: int, background: str | None = None) -> bytes:
    ...
```

Generation spec should support:

```txt
seed
count
style
complexity
stroke_width
palette
background
view_box
motif families
```

Initial style presets:

```txt
Minimal
Tech
Premium UI
Geometric
Mystic
Organic
Dashboard
```

Initial PNG sizes:

```txt
512
1024
2048
4096
```

SVG requirements:

- Valid SVG.
- `viewBox="0 0 48 48"` or scalable equivalent.
- No scripts.
- No external resources.
- No unnecessary background rect for transparent exports.
- Clean deterministic output.
- Easy to recolor.
- Commercially usable visual quality.

Test requirements:

- deterministic output for same seed/spec,
- valid manifest,
- no forbidden SVG tags,
- correct viewBox,
- PNG export dimensions match request,
- snapshot tests for representative glyphs.

---

## 11. API Design

### Public/BFF routes in Next.js

#### `POST /api/generate`

Input:

```json
{
  "seed": "optional",
  "count": 24,
  "style": "premium-ui",
  "complexity": "balanced",
  "stroke": "medium",
  "palette": {
    "stroke": "#9d9788",
    "background": null
  }
}
```

Output:

```json
{
  "jobId": "job_abc123",
  "specHash": "sha256...",
  "glyphs": [
    {
      "glyphId": "glyph_001",
      "name": "target-dot",
      "previewUrl": "/api/preview/job_abc123/glyph_001.png"
    }
  ],
  "expiresAt": "..."
}
```

#### `GET /api/preview/:jobId/:glyphId.png`

Return small preview PNG/WebP, e.g. 512px max.

#### `POST /api/checkout`

Input:

```json
{
  "jobId": "job_abc123",
  "glyphId": "glyph_001",
  "formats": ["svg", "png"],
  "pngSize": 2048,
  "pack": "single"
}
```

Output:

```json
{
  "checkoutUrl": "https://checkout.stripe.com/..."
}
```

#### `POST /api/stripe/webhook`

Must verify Stripe signature. The webhook is the source of truth.

Handle:

```txt
checkout.session.completed
payment_intent.succeeded
payment_intent.payment_failed
charge.refunded, later
```

#### `GET /api/order/:orderId`

Returns order/export status.

#### `GET /api/download/:token`

Tokenized download. Token must be random, hashed in DB, and have TTL.

#### `POST /api/feedback`

Accepts:

```json
{
  "message": "...",
  "useCase": "...",
  "email": "optional",
  "glyphSeed": "optional",
  "rating": "optional"
}
```

Forwards to Telegram when configured.

---

## 12. Stripe Checkout Requirements

Use Stripe Checkout first.

Do not build custom card forms for MVP.

Stripe Checkout should support:

- Apple Pay where available,
- Google Pay where available,
- card payments,
- hosted payment UI,
- success/cancel URLs,
- webhook confirmation.

Order creation flow:

1. Validate request.
2. Create `pending` order in DB.
3. Create Stripe Checkout Session with metadata:

```json
{
  "orderId": "ord_123",
  "jobId": "job_abc123",
  "glyphId": "glyph_001",
  "exportSpecHash": "sha256..."
}
```

4. Redirect user to Stripe.

Webhook flow:

1. Verify signature.
2. Idempotently process event.
3. Mark order `paid`.
4. Generate export files.
5. Create download token.
6. Mark order `downloadsReady`.

Never unlock download solely based on browser redirect.

---

## 13. Storage and Export Pipeline

Use local Docker volume for MVP.

Suggested structure:

```txt
/data/vector-glyphs/
  jobs/
    ab/
      cd/
        job_abc123/
          spec.json
          manifest.json
          previews/
            glyph_001.png
            glyph_002.png
          svg/
            glyph_001.svg
            glyph_002.svg
          exports/
            order_123/
              vector-glyph.svg
              vector-glyph-2048.png
              vector-glyph-pack.zip
              license.txt
```

TTL policy:

```txt
Unpaid generation jobs: 24h
Paid exports: 30 days initially
Order/payment records: keep for accounting/legal needs
```

---

## 14. Security Requirements

### Payment

- Verify Stripe webhook signatures.
- Store processed Stripe event IDs for idempotency.
- Never store card data.
- Never trust client-provided price.
- Price/product must be determined server-side.

### API

- Validate all payloads with Zod/Pydantic.
- Whitelist PNG sizes.
- Whitelist styles.
- Whitelist color format.
- Limit `count`.
- Rate-limit generate/checkout/download/feedback endpoints.
- Keep FastAPI internal if using Next.js as BFF.
- Set CORS narrowly.

### SVG

- No `<script>`.
- No external hrefs.
- No raw user SVG input in MVP.
- Serve paid SVG as attachment.

### Secrets

Use `.env.example`, never commit `.env`.

Required env examples:

```txt
NEXT_PUBLIC_APP_URL=https://vectorglyphs.com
DATABASE_URL=postgresql://...
STRIPE_SECRET_KEY=...
STRIPE_WEBHOOK_SECRET=...
TELEGRAM_BOT_TOKEN=...
TELEGRAM_FEEDBACK_CHAT_ID=...
DOWNLOAD_TOKEN_SECRET=...
POSTGRES_PASSWORD=...
```

---

## 15. Landing Page Structure

### SEO title

```txt
Vector Glyph Generator — Create SVG & PNG Glyphs Online
```

### Meta description

```txt
Generate beautiful circular vector glyphs for apps, websites, logos, UI and digital products. Preview for free, download SVG or high-resolution PNG for $1. Commercial license included.
```

### H1

```txt
Vector Glyph Generator
```

### Hero copy

```txt
Create unique circular SVG and PNG glyphs for apps, websites, logos, dashboards and digital products. Preview for free. Download production-ready files for $1.
```

### Hero microcopy

```txt
No signup required. Commercial license included. SVG and transparent PNG exports.
```

### Main sections

1. Hero + live generator.
2. Generated glyph examples.
3. Use cases in modern UI.
4. SVG/PNG export explanation.
5. Commercial license.
6. How it works.
7. Pricing.
8. FAQ.
9. Feedback form.

### Use cases section

Show examples for:

- app UI ornaments,
- onboarding screens,
- empty states,
- dashboard cards,
- landing page decorations,
- abstract brand marks,
- profile avatars,
- presentation section markers,
- wellness/mindfulness interfaces,
- AI/quant/crypto dashboards.

### FAQ questions

Include:

1. What is a vector glyph generator?
2. Can I download glyphs as SVG?
3. Can I export transparent PNG files?
4. Can I use generated glyphs commercially?
5. Can I use glyphs in logos?
6. Are the glyphs unique?
7. Do I need an account?
8. How much does a download cost?
9. What resolutions are available?
10. Can I request new styles?

---

## 16. Programmatic SEO Roadmap

Later create pages for:

```txt
/svg-glyph-generator
/abstract-icon-generator
/circular-symbol-generator
/geometric-glyph-generator
/ui-glyph-generator
/app-symbol-generator
/logo-glyph-generator
/transparent-png-glyph-generator
/vector-symbol-generator
/sacred-geometry-glyph-generator
/minimal-svg-icon-generator
```

Each page should include:

- specific H1,
- 600–1200 words useful content,
- embedded generator,
- curated examples,
- FAQ,
- internal links,
- CTA to generate/download.

---

## 17. Marketing Strategy

### Channels

Primary:

- Google SEO,
- Product Hunt,
- X/Twitter,
- Indie Hackers,
- Hacker News Show HN,
- Reddit carefully,
- designer inspiration platforms,
- directories for design/dev tools.

Designer platforms to evaluate:

- Dribbble,
- Behance,
- Pinterest,
- Figma Community,
- Layers.to,
- Mobbin-like inspiration submissions where allowed,
- UI8 / Gumroad packs later,
- Product Hunt,
- Uneed,
- BetaList,
- SaaSHub,
- There’s An AI For That only if AI positioning is true/acceptable.

### Content pillars

1. **UI inspiration**
   - “10 ways to use abstract glyphs in SaaS UI”
   - “Empty states with vector glyphs”
   - “Premium onboarding cards with geometric symbols”

2. **Design utility**
   - “SVG vs PNG for UI icons”
   - “How to create visual identity with simple glyphs”

3. **Generated examples**
   - daily glyph,
   - generated glyph pack,
   - app mockup using glyphs,
   - dashboard mockup using glyphs.

4. **Build in public**
   - share progress,
   - share revenue/traffic learnings,
   - share generated designs.

---

## 18. Autonomous Visual Marketing Agent / Skill Concept

The user wants a future Hermes skill/agent that autonomously creates attractive UI inspiration images using VectorGlyphs glyphs and regularly uploads them to design inspiration portals with the VectorGlyphs domain in the caption.

This is a good marketing idea, but implementation must respect platform terms, account/API availability, rate limits, anti-spam rules, and quality thresholds.

### Goal

Create a reusable Hermes skill named something like:

```txt
vectorglyphs-visual-marketing
```

Purpose:

- generate visually impressive UI mockups using VectorGlyphs glyphs,
- render/export high-quality images,
- write captions and hashtags,
- publish or queue posts on approved platforms,
- track URLs and performance,
- learn which visual themes perform best.

### Autonomy mandate

The user's preference is maximum practical autonomy for the marketing system. The system should be designed to run end-to-end without day-to-day human involvement once the user has completed one-time account setup and explicitly enabled publishing.

Use every legitimate automation route available, in this priority order:

1. Official platform API.
2. Platform-supported scheduler/integration.
3. Browser automation through Surfagent / Hermes computer-use for normal UI flows when API is unavailable and the platform/account permits this kind of automation.
4. Upload-ready outbox only when publishing cannot be automated safely or reliably.

Important: autonomy does not mean reckless spam. The agent should maximize automation while preserving account safety, brand quality, rate limits, and platform compliance. Do not bypass CAPTCHAs, access controls, payment walls, or security mechanisms. If a platform requires a one-time manual login/2FA/CAPTCHA, the user can complete that once; after cookies/session are stored, the agent should continue autonomously through Surfagent where practical.

### Important constraints

- The agent may publish fully autonomously only after the user explicitly configures accounts, credentials, platform rules, and an approval policy.
- Some platforms may not allow API upload, automated upload, or commercial automation; check each platform before enabling publishing.
- Browser automation via Surfagent is allowed for ordinary account UI operations where permitted, e.g. opening the platform, filling title/caption/tags, uploading prepared media, selecting category, scheduling/posting, and recording the final URL.
- If a platform blocks automation through CAPTCHA/2FA/manual challenge, the agent should stop and request one-time human completion rather than attempting to bypass the challenge.
- The agent must avoid spammy posting frequency and should use per-platform posting calendars.
- The agent must keep quality high. Poor generated UI images will damage brand perception.

### Recommended approach

Build a layered automation system, but optimize for Level 4 as the default end-state:

#### Level 1 — fully autonomous asset generation

Agent generates:

- UI mockup image,
- glyph set used,
- title,
- caption,
- alt text,
- hashtags,
- source files,
- post metadata JSON.

#### Level 2 — autonomous queue

Agent saves assets into:

```txt
marketing/outbox/
  2026-xx-xx-ui-dashboard-glyphs/
    image.png
    image@2x.png
    caption.md
    metadata.json
    source.html
```

#### Level 3 — autonomous publishing adapters

For each platform, build a `PublisherAdapter`:

```txt
Official API adapter if available
Surfagent browser adapter if API is unavailable but normal UI automation is viable
Manual/outbox adapter only as fallback
```

Each adapter should implement:

```txt
login_check()
prepare_post()
upload_media()
fill_metadata()
publish_or_schedule()
verify_published_url()
record_result()
```

#### Level 4 — performance loop

Agent records:

- post URL,
- date,
- platform,
- impressions if available,
- likes/saves/comments,
- referral clicks,
- notes.

Then adjusts future creative direction.

### Visual content types

Generate recurring visual themes:

1. SaaS dashboard card with glyph category icons.
2. Mobile onboarding screen using a central glyph.
3. Empty state illustration using a glyph.
4. Pricing page visual with premium glyph ornaments.
5. AI/quant dashboard with technical glyph markers.
6. Wellness app screen with calm symbolic glyphs.
7. Landing page hero with abstract glyph background.
8. Brand identity board with glyph mark, colors, typography.
9. Figma-style UI kit preview.
10. “Glyph of the day” poster.

### Generation tools

Prefer deterministic HTML/CSS/SVG mockups rendered with Playwright for consistent quality.

Optional AI image tools can be used for background/texture/inspiration, but for UI design images, HTML/CSS/SVG is often cleaner and more controllable.

Possible pipeline:

```txt
Generate glyph SVGs
↓
Generate UI mockup as HTML/CSS using glyphs
↓
Render 1600×1200 / 2400×1800 PNG with Playwright
↓
Optionally polish background/lighting with image generation if configured
↓
Write caption + alt text
↓
Save to marketing/outbox
↓
Publish to allowed platforms or queue for manual approval
↓
Track result
```

### Platform strategy

Start with channels that are easiest to make fully autonomous and low-risk:

- Own website gallery/blog pages — always automate first; this creates SEO assets and canonical URLs.
- Pinterest — strong visual-discovery channel; use official API/scheduler if available, otherwise evaluate Surfagent UI automation.
- X/Twitter — use API if available; otherwise evaluate browser automation only if account safety is acceptable.
- GitHub examples / open design assets — easy to automate through git.
- Figma Community — evaluate API/manual requirements; likely needs a dedicated adapter or upload-ready package.
- Dribbble and Behance — high-value design channels; research current upload/API/browser automation feasibility, then build adapters if practical.
- Additional design/inspiration directories discovered by Marketing Scout.

For every platform create a `docs/marketing/platforms/<platform>.md` file containing:

```txt
login/setup requirements
API availability
Surfagent browser automation feasibility
posting limits/frequency
required image dimensions
caption/tag rules
risk level
adapter status
```

Treat Dribbble/Behance as priority targets, but implement them with account-safety checks:

- verify current API/upload support and ToS,
- if API is unavailable, create a Surfagent adapter for the normal browser upload flow where feasible,
- persist browser/session state after user completes any required one-time login/2FA,
- stop rather than bypass CAPTCHA/security challenges,
- always verify the final published URL and record it.

### Skill output requirements

Every marketing run should produce:

```txt
marketing/outbox/<date-slug>/image.png
marketing/outbox/<date-slug>/caption.md
marketing/outbox/<date-slug>/alt-text.md
marketing/outbox/<date-slug>/metadata.json
marketing/outbox/<date-slug>/source.html
```

Metadata fields:

```json
{
  "title": "...",
  "theme": "dashboard|onboarding|empty-state|brand-board|poster",
  "glyphSeed": "...",
  "targetPlatforms": ["pinterest", "x", "dribbble"],
  "caption": "...",
  "hashtags": ["..."],
  "domainMention": "vectorglyphs.com",
  "status": "draft|queued|published|failed",
  "publishedUrls": []
}
```

### Quality gate

Before publishing, automatically evaluate:

- visual polish,
- legibility,
- no broken layout,
- glyph visible and attractive,
- domain/caption present but not obnoxious,
- no hallucinated UI claims,
- no trademark/copyrighted brand imitation,
- no spammy hashtags.

If score is below threshold, do not publish; regenerate or queue for review.

---

## 19. Autonomous Cron Jobs to Create Later

Do not create these until the repo exists and the user approves.

### Daily Project Manager

Schedule:

```txt
every day 09:00
```

Task:

- read `BACKLOG.md`, `ROADMAP.md`, `PROJECT_BRIEF.md`,
- propose top 3 tasks,
- optionally implement only if approval policy allows,
- never touch other repos.

### Daily Marketing Scout

Schedule:

```txt
every day 11:00
```

Task:

- search design/dev trends,
- find content/promotional opportunities,
- propose post ideas,
- save drafts.

### Visual Marketing Generator

Schedule:

```txt
3x per week initially
```

Task:

- generate one high-quality UI inspiration visual using VectorGlyphs glyphs,
- save image/caption/metadata to `marketing/outbox`,
- publish only to approved platforms with configured credentials and explicit policy.

### SEO Page Planner

Schedule:

```txt
weekly
```

Task:

- propose SEO pages,
- generate outlines,
- draft content,
- do not publish without approval unless policy allows.

### Deployment Watchdog

Schedule:

```txt
every 30m
```

Task:

- check public health endpoint,
- alert only when down,
- stay silent when OK.

---

## 20. Development Phases

### Phase 0 — Project foundation

Tasks:

- create repo structure,
- add docs:
  - `AGENTS.md`,
  - `PROJECT_BRIEF.md`,
  - `BUSINESS_PLAN.md`,
  - `ROADMAP.md`,
  - `BACKLOG.md`,
  - `DEPLOYMENT.md`,
  - `MARKETING_PLAN.md`,
- add `.gitignore`, `.env.example`, README,
- make first clean commit.

### Phase 1 — Extract glyph core

Tasks:

- copy original generator into repo as reference,
- refactor into `glyph_core`,
- add tests,
- generate sample gallery,
- confirm deterministic output,
- confirm SVG validity.

### Phase 2 — Web MVP without payment

Tasks:

- scaffold Next.js app,
- create premium landing page,
- add live generator preview,
- add style/color/size controls,
- add generated examples,
- add SEO metadata and FAQ,
- add feedback form stub.

### Phase 3 — Export backend

Tasks:

- scaffold FastAPI app,
- expose generation endpoint,
- expose export endpoint,
- implement PNG export,
- implement ZIP export,
- add health checks,
- add integration tests.

### Phase 4 — Stripe payment

Tasks:

- implement pending orders,
- implement Stripe Checkout,
- implement webhook,
- implement success page,
- implement tokenized download,
- test in Stripe test mode.

### Phase 5 — Docker deployment

Tasks:

- create Dockerfiles,
- create Docker Compose,
- run locally,
- prepare production compose,
- prepare Caddy/Traefik config,
- prepare Cloudflare Tunnel docs,
- deploy to LAN host after user provides access/approval.

### Phase 6 — SEO and launch

Tasks:

- connect Search Console,
- add sitemap/robots,
- add programmatic SEO pages,
- create launch assets,
- prepare Product Hunt / HN / Reddit / X copy,
- create analytics dashboard.

### Phase 7 — Autonomous visual marketing

Tasks:

- create `vectorglyphs-visual-marketing` skill,
- build HTML/CSS/SVG UI mockup generator,
- render images with Playwright,
- create outbox format,
- add quality gate,
- add platform adapters only where safe/API-supported,
- create marketing cron after approval.

---

## 21. Initial Backlog

Create `BACKLOG.md` with these initial items.

### Foundation

- [ ] Create project skeleton.
- [ ] Add AGENTS.md with project boundaries.
- [ ] Add product brief.
- [ ] Add business plan.
- [ ] Add roadmap.
- [ ] Add deployment plan.
- [ ] Add marketing plan.
- [ ] Add .env.example.

### Generator

- [ ] Import original generator as reference.
- [ ] Refactor generator into `glyph_core`.
- [ ] Add seed-based generation.
- [ ] Add palette controls.
- [ ] Add complexity controls.
- [ ] Add SVG validation tests.
- [ ] Add PNG export tests.

### Web

- [ ] Scaffold Next.js app.
- [ ] Build hero section.
- [ ] Build live generator UI.
- [ ] Build examples grid.
- [ ] Build use-case sections.
- [ ] Build FAQ.
- [ ] Build feedback form.

### Payments

- [ ] Add Postgres schema for orders.
- [ ] Add Stripe Checkout session creation.
- [ ] Add Stripe webhook.
- [ ] Add tokenized download.
- [ ] Add success page.

### Deployment

- [ ] Add Docker Compose.
- [ ] Add production compose.
- [ ] Add Caddy/Traefik config.
- [ ] Add Cloudflare Tunnel instructions.
- [ ] Add health endpoint.

### Marketing

- [ ] Create SEO keyword list.
- [ ] Draft first 10 SEO pages.
- [ ] Draft Product Hunt copy.
- [ ] Draft HN Show HN post.
- [ ] Draft X launch thread.
- [ ] Design first 10 UI inspiration images.
- [ ] Create visual marketing skill spec.

---

## 22. Verification Commands

As implementation proceeds, maintain commands like:

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

Adjust paths/scripts after actual scaffolding.

---

## 23. First Instruction for the New Hermes Session

When starting the new project session, give Hermes this instruction:

```txt
You are now working on the independent VectorGlyphs project in this directory. Read VECTORGLYPHS_MASTER_PROMPT.md completely, then execute Phase 0 only: create the project skeleton and documentation files described in the prompt. Do not implement the web app yet, do not touch other repositories, do not spend money, do not deploy, and do not create cron jobs yet. After Phase 0, summarize what you created and propose the Phase 1 plan.
```

After Phase 0 succeeds, continue with:

```txt
Execute Phase 1 from VECTORGLYPHS_MASTER_PROMPT.md: import/refactor the glyph generator into a standalone glyph_core package with tests. Keep all work inside this repository.
```

Proceed phase by phase. Do not ask the agent to “do everything” in one uncontrolled pass; that increases risk. The goal is autonomous execution with clear gates.

---

## 24. Final Strategic Summary

VectorGlyphs should be built as a focused, premium micro-product:

```txt
Free previews → $1 SVG/PNG download → packs/credits → SEO + visual marketing loop.
```

The strongest technical path:

```txt
Next.js + FastAPI + glyph_core + Stripe Checkout + Docker Compose + Cloudflare Tunnel.
```

The strongest growth path:

```txt
SEO pages + generated UI inspiration visuals + daily/weekly glyph content + design/dev community distribution.
```

The strongest operating model:

```txt
Separate repo, separate Hermes profile, separate AGENTS.md, separate backlog, separate crons, strict no-cross-contamination with PowerAppMVP2.
```

The product is promising because the glyph generator is visually strong, practical, cheap to serve, SEO-friendly, and naturally reusable for marketing visuals.
