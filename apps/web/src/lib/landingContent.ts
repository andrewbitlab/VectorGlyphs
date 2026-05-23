export const HERO_COPY = {
  title: "Vector Glyph Generator",
  description:
    "Create unique circular SVG and PNG glyphs for apps, websites, logos, dashboards and digital products. Generate a premium icon language in seconds, then see it live inside real product surfaces.",
  microcopy: "No signup required. Commercial license included. Payment-confirmed SVG, PNG and ZIP exports.",
};

export const LANDING_SECTIONS = [
  { id: "hero-generator", label: "Hero + live generator" },
  { id: "examples", label: "Generated glyph examples" },
  { id: "studio", label: "Premium retention studio" },
  { id: "in-context", label: "Glyphs in product context" },
  { id: "use-cases", label: "Use cases in modern UI" },
  { id: "exports", label: "SVG/PNG export explanation" },
  { id: "license", label: "Commercial license" },
  { id: "how-it-works", label: "How it works" },
  { id: "pricing", label: "Pricing" },
  { id: "faq", label: "FAQ" },
  { id: "feedback", label: "Feedback form" },
] as const;

export const USE_CASES = [
  "App UI ornaments",
  "Onboarding screens",
  "Empty states",
  "Dashboard cards",
  "Landing page decorations",
  "Abstract brand marks",
  "Profile avatars",
  "Presentation section markers",
  "Wellness / mindfulness interfaces",
  "AI / quant / crypto dashboards",
] as const;

export const RETENTION_FEATURES = [
  {
    title: "Explore variations",
    body: "One click keeps the creative loop moving: fresh sets, retained style direction, and enough contrast to make comparison addictive.",
  },
  {
    title: "Build a keeper set",
    body: "The interface frames generated marks as a curated product asset system instead of one-off clipart, nudging users to assemble a reusable set.",
  },
  {
    title: "Preview in context",
    body: "Glyphs appear inside onboarding cards, dashboard modules, and brand tiles so users instantly imagine where they would use them.",
  },
  {
    title: "Export with confidence",
    body: "The purchase path reinforces clean SVG, transparent PNG, ZIP bundles, licensing clarity, and webhook-confirmed fulfillment.",
  },
] as const;

export const IN_CONTEXT_SHOWCASES = [
  {
    title: "App onboarding",
    body: "Use glyph marks as calm, premium illustrations for onboarding steps, empty states, and feature education screens.",
  },
  {
    title: "Dashboard cards",
    body: "Use glyph accents to separate metrics, alerts, automations, and data views without relying on generic icon packs.",
  },
  {
    title: "Brand system tiles",
    body: "Turn a glyph set into a consistent visual language for landing pages, pitch decks, changelogs, and internal tools.",
  },
] as const;

export const FAQ_ITEMS = [
  {
    question: "What is a vector glyph generator?",
    answer: "It is a procedural design tool that creates scalable symbolic marks for digital interfaces and product visuals.",
  },
  {
    question: "Can I download glyphs as SVG?",
    answer: "Yes. The export backend can package clean SVG files after a payment-confirmed checkout flow.",
  },
  {
    question: "Can I export transparent PNG files?",
    answer: "Yes. The export backend supports transparent PNG files at 512, 1024, 2048 and 4096 pixels.",
  },
  {
    question: "Can I use generated glyphs commercially?",
    answer: "Purchased glyphs include commercial use for apps, websites, presentations, UI kits and digital products.",
  },
  {
    question: "Can I use glyphs in logos?",
    answer: "You may use purchased glyphs as brand elements, but VectorGlyphs does not guarantee trademark uniqueness or registrability.",
  },
  {
    question: "Are the glyphs unique?",
    answer: "Each glyph is procedurally generated from a large design space, making results highly varied without claiming absolute uniqueness.",
  },
  {
    question: "Do I need an account?",
    answer: "No. The MVP is designed around previewing and purchasing exports without account creation.",
  },
  {
    question: "How much does a download cost?",
    answer: "The planned starting price is $1 for a production export pack, with pricing experiments planned later.",
  },
  {
    question: "What resolutions are available?",
    answer: "PNG sizes are 512, 1024, 2048 and 4096 pixels.",
  },
  {
    question: "Can I request new styles?",
    answer: "Yes. The feedback form captures requested styles and use cases before Telegram forwarding is configured.",
  },
] as const;

export type FeedbackDraft = {
  message?: string;
  useCase?: string;
  email?: string;
};

export type FeedbackValidation = { ok: true } | { ok: false; error: string };

export function validateFeedbackDraft(draft: FeedbackDraft): FeedbackValidation {
  const message = draft.message?.trim() ?? "";
  if (message.length < 10) {
    return { ok: false, error: "Feedback message must be at least 10 characters." };
  }
  if (draft.email && !draft.email.includes("@")) {
    return { ok: false, error: "Email must be valid when provided." };
  }
  return { ok: true };
}
