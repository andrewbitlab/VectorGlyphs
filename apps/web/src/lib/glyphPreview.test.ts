import { describe, expect, it } from "vitest";

import {
  buildPreviewSpec,
  generatePreviewGlyphs,
  renderPreviewSvg,
  STYLE_PRESETS,
  PNG_SIZES,
} from "./glyphPreview";

describe("glyph preview generation", () => {
  it("generates deterministic glyph previews for the same seed and controls", () => {
    const spec = buildPreviewSpec({ seed: "phase-2", style: "premium-ui", complexity: "balanced", count: 6 });

    const first = generatePreviewGlyphs(spec);
    const second = generatePreviewGlyphs(spec);

    expect(first.map((glyph) => glyph.id)).toEqual(["glyph_001", "glyph_002", "glyph_003", "glyph_004", "glyph_005", "glyph_006"]);
    expect(first.map((glyph) => glyph.name)).toEqual(second.map((glyph) => glyph.name));
    expect(first.map((glyph) => renderPreviewSvg(glyph, spec))).toEqual(second.map((glyph) => renderPreviewSvg(glyph, spec)));
  });

  it("changes preview output when the seed changes", () => {
    const first = buildPreviewSpec({ seed: "phase-2-a", style: "tech", complexity: "balanced", count: 3 });
    const second = buildPreviewSpec({ seed: "phase-2-b", style: "tech", complexity: "balanced", count: 3 });

    expect(renderPreviewSvg(generatePreviewGlyphs(first)[0], first)).not.toEqual(
      renderPreviewSvg(generatePreviewGlyphs(second)[0], second),
    );
  });

  it("renders clean recolorable SVG without scripts or external hrefs", () => {
    const spec = buildPreviewSpec({ seed: "clean-svg", stroke: "#9d9788", background: "transparent" });
    const svg = renderPreviewSvg(generatePreviewGlyphs(spec)[0], spec);

    expect(svg).toContain('viewBox="0 0 48 48"');
    expect(svg).toContain("currentColor");
    expect(svg).not.toContain("<script");
    expect(svg).not.toContain("href=");
    expect(svg).not.toContain("<rect");
  });

  it("exposes the MVP control option sets", () => {
    expect(STYLE_PRESETS.map((style) => style.value)).toEqual([
      "minimal",
      "tech",
      "premium-ui",
      "geometric",
      "mystic",
      "organic",
      "dashboard",
    ]);
    expect(PNG_SIZES).toEqual([512, 1024, 2048, 4096]);
  });

  it("validates count, colors, style, and png size", () => {
    expect(() => buildPreviewSpec({ count: 0 })).toThrow(/count/i);
    expect(() => buildPreviewSpec({ style: "unsupported" })).toThrow(/style/i);
    expect(() => buildPreviewSpec({ stroke: "gold" })).toThrow(/color/i);
    expect(() => buildPreviewSpec({ pngSize: 300 })).toThrow(/PNG size/i);
  });
});
