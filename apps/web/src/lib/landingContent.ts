export const HERO_COPY = {
  title: "Vector Glyph Generator",
  description:
    "Create unique circular SVG and PNG glyphs for apps, websites, logos, dashboards and digital products. Preview for free. Download production-ready files for $1.",
  microcopy: "No signup required. Commercial license included. SVG and transparent PNG exports.",
};

export const LANDING_SECTIONS = [
  { id: "hero-generator", label: "Hero + live generator" },
  { id: "examples", label: "Generated glyph examples" },
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

export const FAQ_ITEMS = [
  {
    question: "What is a vector glyph generator?",
    answer: "It is a procedural design tool that creates scalable symbolic marks for digital interfaces and product visuals.",
  },
  {
    question: "Can I download glyphs as SVG?",
    answer: "Yes. SVG export is part of the paid MVP path; Phase 2 previews the flow without payment.",
  },
  {
    question: "Can I export transparent PNG files?",
    answer: "Yes. The planned export backend supports transparent PNG files at production resolutions.",
  },
  {
    question: "Can I use generated glyphs commercially?",
    answer: "Purchased glyphs will include commercial use for apps, websites, presentations, UI kits and digital products.",
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
    answer: "The planned starting price is $1 for a single glyph export, with export packs tested later.",
  },
  {
    question: "What resolutions are available?",
    answer: "The planned PNG sizes are 512, 1024, 2048 and 4096 pixels.",
  },
  {
    question: "Can I request new styles?",
    answer: "Yes. The Phase 2 feedback form captures requested styles and use cases before Telegram forwarding is configured.",
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
