import { describe, expect, it } from "vitest";

import {
  FAQ_ITEMS,
  HERO_COPY,
  IN_CONTEXT_SHOWCASES,
  LANDING_SECTIONS,
  RETENTION_FEATURES,
  USE_CASES,
  validateFeedbackDraft,
} from "./landingContent";

describe("landing content", () => {
  it("uses the SEO copy from the master product positioning", () => {
    expect(HERO_COPY.title).toBe("Vector Glyph Generator");
    expect(HERO_COPY.description).toContain("Create unique circular SVG and PNG glyphs");
    expect(HERO_COPY.microcopy).toContain("No signup required");
    expect(HERO_COPY.microcopy).toContain("Commercial license included");
  });

  it("covers the required landing sections", () => {
    expect(LANDING_SECTIONS.map((section) => section.id)).toEqual([
      "hero-generator",
      "examples",
      "studio",
      "in-context",
      "use-cases",
      "exports",
      "license",
      "how-it-works",
      "pricing",
      "faq",
      "feedback",
    ]);
  });

  it("includes core use cases and FAQ questions", () => {
    expect(USE_CASES).toContain("Dashboard cards");
    expect(USE_CASES).toContain("AI / quant / crypto dashboards");
    expect(FAQ_ITEMS.map((item) => item.question)).toContain("Can I download glyphs as SVG?");
    expect(FAQ_ITEMS.map((item) => item.question)).toContain("How much does a download cost?");
  });

  it("defines premium retention content that pushes users to use glyphs in real product surfaces", () => {
    expect(RETENTION_FEATURES.map((feature) => feature.title)).toEqual([
      "Explore variations",
      "Build a keeper set",
      "Preview in context",
      "Export with confidence",
    ]);
    expect(IN_CONTEXT_SHOWCASES.map((showcase) => showcase.title)).toEqual([
      "App onboarding",
      "Dashboard cards",
      "Brand system tiles",
    ]);
    expect(IN_CONTEXT_SHOWCASES.every((showcase) => showcase.body.includes("glyph"))).toBe(true);
  });

  it("validates feedback drafts before future Telegram forwarding", () => {
    expect(validateFeedbackDraft({ message: "Please add fintech dashboard presets", useCase: "Dashboard" })).toEqual({
      ok: true,
    });
    expect(validateFeedbackDraft({ message: "short" })).toEqual({
      ok: false,
      error: "Feedback message must be at least 10 characters.",
    });
  });
});
