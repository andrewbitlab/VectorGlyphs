import { describe, expect, it } from "vitest";

import {
  FAQ_ITEMS,
  HERO_COPY,
  LANDING_SECTIONS,
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
