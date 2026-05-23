export const STYLE_PRESETS = [
  { value: "minimal", label: "Minimal" },
  { value: "tech", label: "Tech" },
  { value: "premium-ui", label: "Premium UI" },
  { value: "geometric", label: "Geometric" },
  { value: "mystic", label: "Mystic" },
  { value: "organic", label: "Organic" },
  { value: "dashboard", label: "Dashboard" },
] as const;

export const COMPLEXITY_PRESETS = [
  { value: "simple", label: "Simple" },
  { value: "balanced", label: "Balanced" },
  { value: "dense", label: "Dense" },
] as const;

export const PNG_SIZES = [512, 1024, 2048, 4096] as const;

export type GlyphStyle = (typeof STYLE_PRESETS)[number]["value"];
export type GlyphComplexity = (typeof COMPLEXITY_PRESETS)[number]["value"];
export type PngSize = (typeof PNG_SIZES)[number];
export type BackgroundMode = "transparent" | "dark" | "light";
export type ExportFormat = "svg" | "png" | "zip";

export type PreviewSpecInput = Partial<{
  seed: string;
  count: number;
  style: string;
  complexity: string;
  stroke: string;
  background: BackgroundMode;
  pngSize: number;
  format: ExportFormat;
}>;

export type PreviewSpec = {
  seed: string;
  count: number;
  style: GlyphStyle;
  complexity: GlyphComplexity;
  stroke: string;
  background: BackgroundMode;
  pngSize: PngSize;
  format: ExportFormat;
  viewBox: "0 0 48 48";
};

export type PreviewGlyph = {
  id: string;
  name: string;
  template: string;
  tags: string[];
  elements: string[];
};

type GlyphTemplate = {
  name: string;
  tags: string[];
  draw: () => string[];
};

const HEX_COLOR = /^#[0-9a-fA-F]{6}([0-9a-fA-F]{2})?$/;
const CENTER = 24;
const RADIUS = 17.6;
const BASE_STROKE = 3.6;
const INNER_STROKE = 2.65;
const BOLD_STROKE = 4.35;

function assertColor(value: string): void {
  if (!HEX_COLOR.test(value)) {
    throw new Error("Stroke color must be a hex color like #9d9788.");
  }
}

function assertStyle(value: string): asserts value is GlyphStyle {
  if (!STYLE_PRESETS.some((style) => style.value === value)) {
    throw new Error("Unsupported style preset.");
  }
}

function assertComplexity(value: string): asserts value is GlyphComplexity {
  if (!COMPLEXITY_PRESETS.some((complexity) => complexity.value === value)) {
    throw new Error("Unsupported complexity preset.");
  }
}

function assertPngSize(value: number): asserts value is PngSize {
  if (!PNG_SIZES.includes(value as PngSize)) {
    throw new Error("PNG size must be one of 512, 1024, 2048, or 4096.");
  }
}

export function buildPreviewSpec(input: PreviewSpecInput = {}): PreviewSpec {
  const style = input.style ?? "premium-ui";
  const complexity = input.complexity ?? "balanced";
  const stroke = input.stroke ?? "#9d9788";
  const count = input.count ?? 12;
  const pngSize = input.pngSize ?? 2048;

  assertStyle(style);
  assertComplexity(complexity);
  assertColor(stroke);
  assertPngSize(pngSize);
  if (count < 1 || count > 24) {
    throw new Error("Preview count must be between 1 and 24.");
  }

  return {
    seed: input.seed?.trim() || "vectorglyphs-demo",
    count,
    style,
    complexity,
    stroke,
    background: input.background ?? "transparent",
    pngSize,
    format: input.format ?? "svg",
    viewBox: "0 0 48 48",
  };
}

function fmt(value: number): string {
  const text = value.toFixed(4).replace(/0+$/, "").replace(/\.$/, "");
  return text === "-0" ? "0" : text;
}

function polar(radius: number, angleDeg: number): [number, number] {
  const angle = ((angleDeg - 90) * Math.PI) / 180;
  return [CENTER + radius * Math.cos(angle), CENTER + radius * Math.sin(angle)];
}

function opacity(opacityValue = 1): string {
  return opacityValue === 1 ? "" : ` opacity="${fmt(opacityValue)}"`;
}

function arcPath(startDeg: number, endDeg: number, radius = RADIUS): string {
  let span = (endDeg - startDeg) % 360;
  if (span < 0) span += 360;
  if (span === 0) span = 359.999;
  const [sx, sy] = polar(radius, startDeg);
  const [ex, ey] = polar(radius, startDeg + span);
  const largeArc = span > 180 ? 1 : 0;
  return `M ${fmt(sx)} ${fmt(sy)} A ${fmt(radius)} ${fmt(radius)} 0 ${largeArc} 1 ${fmt(ex)} ${fmt(ey)}`;
}

function circle(radius = RADIUS, width = BASE_STROKE, opacityValue = 1): string {
  return `<circle cx="24" cy="24" r="${fmt(radius)}" fill="none" stroke="currentColor" stroke-width="${fmt(width)}" stroke-linecap="round" stroke-linejoin="round"${opacity(opacityValue)}/>`;
}

function arc(start: number, end: number, width = BASE_STROKE, radius = RADIUS, opacityValue = 1): string {
  return `<path d="${arcPath(start, end, radius)}" fill="none" stroke="currentColor" stroke-width="${fmt(width)}" stroke-linecap="round" stroke-linejoin="round"${opacity(opacityValue)}/>`;
}

function line(angle: number, length: number, width = BOLD_STROKE, opacityValue = 1): string {
  const [x1, y1] = polar(length / 2, angle);
  const [x2, y2] = polar(length / 2, angle + 180);
  return `<line x1="${fmt(x1)}" y1="${fmt(y1)}" x2="${fmt(x2)}" y2="${fmt(y2)}" stroke="currentColor" stroke-width="${fmt(width)}" stroke-linecap="round"${opacity(opacityValue)}/>`;
}

function hline(yOffset: number, length: number, width = INNER_STROKE): string {
  const y = CENTER + yOffset;
  return `<line x1="${fmt(CENTER - length / 2)}" y1="${fmt(y)}" x2="${fmt(CENTER + length / 2)}" y2="${fmt(y)}" stroke="currentColor" stroke-width="${fmt(width)}" stroke-linecap="round"/>`;
}

function vline(xOffset: number, length: number, width = INNER_STROKE): string {
  const x = CENTER + xOffset;
  return `<line x1="${fmt(x)}" y1="${fmt(CENTER - length / 2)}" x2="${fmt(x)}" y2="${fmt(CENTER + length / 2)}" stroke="currentColor" stroke-width="${fmt(width)}" stroke-linecap="round"/>`;
}

function dot(angle: number, radiusFromCenter = RADIUS, dotRadius = 2, opacityValue = 1): string {
  const [x, y] = polar(radiusFromCenter, angle);
  return `<circle cx="${fmt(x)}" cy="${fmt(y)}" r="${fmt(dotRadius)}" fill="currentColor"${opacity(opacityValue)}/>`;
}

function centerDot(radius = 3, opacityValue = 1): string {
  return `<circle cx="24" cy="24" r="${fmt(radius)}" fill="currentColor"${opacity(opacityValue)}/>`;
}

function diamond(size = 15, width = INNER_STROKE): string {
  const half = size / 2;
  const d = `M 24 ${fmt(24 - half)} L ${fmt(24 + half)} 24 L 24 ${fmt(24 + half)} L ${fmt(24 - half)} 24 Z`;
  return `<path d="${d}" fill="none" stroke="currentColor" stroke-width="${fmt(width)}" stroke-linecap="round" stroke-linejoin="round"/>`;
}

function orbitDots(angles: number[], radius = RADIUS, dotRadius = 1.85, opacityValue = 1): string[] {
  return angles.map((angle) => dot(angle, radius, dotRadius, opacityValue));
}

function templates(): GlyphTemplate[] {
  const cardinal = [0, 90, 180, 270];
  const diagonal = [45, 135, 225, 315];
  const octants = [0, 45, 90, 135, 180, 225, 270, 315];
  return [
    { name: "silence-ring", tags: ["minimal", "simple"], draw: () => [circle()] },
    { name: "vertical-mark", tags: ["minimal", "simple"], draw: () => [circle(), line(0, 27)] },
    { name: "horizontal-mark", tags: ["minimal", "simple"], draw: () => [circle(), line(90, 27)] },
    { name: "parallel-vertical-bars", tags: ["dashboard", "balanced"], draw: () => [circle(), vline(-5, 21, 2.9), vline(5, 21, 2.9)] },
    { name: "diagonal-slash", tags: ["tech", "simple"], draw: () => [circle(), line(45, 27)] },
    { name: "target-dot", tags: ["tech", "balanced"], draw: () => [circle(), circle(7.8, 3.1, 0.88), centerDot(3.35, 0.82)] },
    { name: "vertical-dot-core", tags: ["premium-ui", "balanced"], draw: () => [circle(), ...orbitDots([0, 180], 12.2, 2.75, 0.92), centerDot(1.95, 0.82)] },
    { name: "horizontal-dot-core", tags: ["premium-ui", "balanced"], draw: () => [circle(), ...orbitDots([90, 270], 12.2, 2.75, 0.92), centerDot(1.95, 0.82)] },
    { name: "inner-pulse-core", tags: ["premium-ui", "balanced"], draw: () => [circle(), circle(8.8, 2.45, 0.74), centerDot(2.55, 0.88)] },
    { name: "four-inner-dots", tags: ["premium-ui", "dense"], draw: () => [circle(), ...orbitDots(cardinal, 12.8, 2.55, 0.9)] },
    { name: "inner-diamond", tags: ["geometric", "simple"], draw: () => [circle(), diamond(15.5, 3.35)] },
    { name: "halo-four-dots", tags: ["geometric", "dense"], draw: () => [circle(), circle(10.4, 2.95, 0.82), ...orbitDots(cardinal, 9.4, 2.25, 0.88)] },
    { name: "cardinal-dot-core", tags: ["mystic", "dense"], draw: () => [circle(), ...orbitDots(cardinal, 11, 2, 0.92), centerDot(2.15, 0.86)] },
    { name: "diagonal-dot-core", tags: ["mystic", "dense"], draw: () => [circle(), ...orbitDots(diagonal, 11.2, 1.85, 0.9), centerDot(2.15, 0.86)] },
    { name: "filled-vertical-crescents", tags: ["organic", "balanced"], draw: () => [circle(), arc(312, 48, 3.45, 9.2), arc(132, 228, 3.45, 9.2), centerDot(1.95, 0.84)] },
    { name: "filled-horizontal-crescents", tags: ["organic", "balanced"], draw: () => [circle(), arc(42, 138, 3.45, 9.2), arc(222, 318, 3.45, 9.2), centerDot(1.95, 0.84)] },
    { name: "three-horizontal-bars", tags: ["dashboard", "dense"], draw: () => [circle(), hline(-6.5, 22.5, 3.15), hline(0, 22.5, 3.15), hline(6.5, 22.5, 3.15)] },
    { name: "octant-dot-core", tags: ["mystic", "dense"], draw: () => [circle(), ...orbitDots(octants, 10.8, 1.62, 0.9), centerDot(1.85, 0.82)] },
  ];
}

function hashString(value: string): number {
  let hash = 2166136261;
  for (let index = 0; index < value.length; index += 1) {
    hash ^= value.charCodeAt(index);
    hash = Math.imul(hash, 16777619);
  }
  return hash >>> 0;
}

function shuffle<T>(items: T[], seed: string): T[] {
  const result = [...items];
  let state = hashString(seed) || 1;
  for (let index = result.length - 1; index > 0; index -= 1) {
    state = Math.imul(1664525, state) + 1013904223;
    const swap = (state >>> 0) % (index + 1);
    [result[index], result[swap]] = [result[swap], result[index]];
  }
  return result;
}

function rank(template: GlyphTemplate): number {
  if (template.tags.includes("simple")) return 1;
  if (template.tags.includes("dense")) return 3;
  return 2;
}

function orderedTemplates(spec: PreviewSpec): GlyphTemplate[] {
  const base = templates().filter((template) => {
    if (spec.complexity === "simple") return rank(template) <= 2;
    if (spec.complexity === "dense") return rank(template) >= 2;
    return true;
  });
  const styleMatches = base.filter((template) => template.tags.includes(spec.style));
  const rest = base.filter((template) => !template.tags.includes(spec.style));
  return [
    ...shuffle(styleMatches, `${spec.seed}|${spec.style}|style`),
    ...shuffle(rest, `${spec.seed}|${spec.complexity}|rest`),
  ];
}

export function generatePreviewGlyphs(spec: PreviewSpec): PreviewGlyph[] {
  const ordered = orderedTemplates(spec);
  return Array.from({ length: spec.count }, (_, index) => {
    const template = ordered[index % ordered.length];
    const cycle = Math.floor(index / ordered.length);
    const name = cycle === 0 ? template.name : `${template.name}-${cycle + 1}`;
    return {
      id: `glyph_${String(index + 1).padStart(3, "0")}`,
      name,
      template: template.name,
      tags: template.tags,
      elements: template.draw(),
    };
  });
}

function backgroundFill(mode: BackgroundMode): string | null {
  if (mode === "dark") return "#050a08";
  if (mode === "light") return "#f7f1df";
  return null;
}

export function renderPreviewSvg(glyph: PreviewGlyph, spec: PreviewSpec): string {
  const bg = backgroundFill(spec.background);
  const background = bg ? `  <rect width="48" height="48" fill="${bg}"/>\n` : "";
  return `<svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="${spec.viewBox}" role="img" aria-label="${glyph.name}" color="${spec.stroke}">\n${background}  <g id="${glyph.id}" data-name="${glyph.name}" vector-effect="non-scaling-stroke">\n    ${glyph.elements.join("\n    ")}\n  </g>\n</svg>`;
}
