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
const MAX_PREVIEW_COUNT = 50;

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
  if (count < 1 || count > MAX_PREVIEW_COUNT) {
    throw new Error(`Preview count must be between 1 and ${MAX_PREVIEW_COUNT}.`);
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

function filledCircle(radius = 3, opacityValue = 1): string {
  return `<circle cx="24" cy="24" r="${fmt(radius)}" fill="currentColor"${opacity(opacityValue)}/>`;
}

function arc(start: number, end: number, width = BASE_STROKE, radius = RADIUS, opacityValue = 1): string {
  return `<path d="${arcPath(start, end, radius)}" fill="none" stroke="currentColor" stroke-width="${fmt(width)}" stroke-linecap="round" stroke-linejoin="round"${opacity(opacityValue)}/>`;
}

function ringSegments(segments: Array<[number, number]>, radius = RADIUS, width = BASE_STROKE, opacityValue = 1): string[] {
  return segments.map(([start, end]) => arc(start, end, width, radius, opacityValue));
}

function line(angle: number, length: number, width = BOLD_STROKE, opacityValue = 1): string {
  const [x1, y1] = polar(length / 2, angle);
  const [x2, y2] = polar(length / 2, angle + 180);
  return `<line x1="${fmt(x1)}" y1="${fmt(y1)}" x2="${fmt(x2)}" y2="${fmt(y2)}" stroke="currentColor" stroke-width="${fmt(width)}" stroke-linecap="round"${opacity(opacityValue)}/>`;
}

function hline(yOffset: number, length: number, width = INNER_STROKE, opacityValue = 1): string {
  const y = CENTER + yOffset;
  return `<line x1="${fmt(CENTER - length / 2)}" y1="${fmt(y)}" x2="${fmt(CENTER + length / 2)}" y2="${fmt(y)}" stroke="currentColor" stroke-width="${fmt(width)}" stroke-linecap="round"${opacity(opacityValue)}/>`;
}

function vline(xOffset: number, length: number, width = INNER_STROKE, opacityValue = 1): string {
  const x = CENTER + xOffset;
  return `<line x1="${fmt(x)}" y1="${fmt(CENTER - length / 2)}" x2="${fmt(x)}" y2="${fmt(CENTER + length / 2)}" stroke="currentColor" stroke-width="${fmt(width)}" stroke-linecap="round"${opacity(opacityValue)}/>`;
}

function shortLine(cx: number, cy: number, dx: number, dy: number, width = INNER_STROKE, opacityValue = 1): string {
  return `<line x1="${fmt(cx - dx)}" y1="${fmt(cy - dy)}" x2="${fmt(cx + dx)}" y2="${fmt(cy + dy)}" stroke="currentColor" stroke-width="${fmt(width)}" stroke-linecap="round"${opacity(opacityValue)}/>`;
}

function dot(angle: number, radiusFromCenter = 11, dotRadius = 2, opacityValue = 1): string {
  const [x, y] = polar(radiusFromCenter, angle);
  return `<circle cx="${fmt(x)}" cy="${fmt(y)}" r="${fmt(dotRadius)}" fill="currentColor"${opacity(opacityValue)}/>`;
}

function centerDot(radius = 3, opacityValue = 1): string {
  return filledCircle(radius, opacityValue);
}

function polygon(points: Array<[number, number]>, width = INNER_STROKE, opacityValue = 1, fill = "none"): string {
  const [first, ...rest] = points;
  const d = [`M ${fmt(first[0])} ${fmt(first[1])}`, ...rest.map(([x, y]) => `L ${fmt(x)} ${fmt(y)}`), "Z"].join(" ");
  return `<path d="${d}" fill="${fill}" stroke="currentColor" stroke-width="${fmt(width)}" stroke-linecap="round" stroke-linejoin="round"${opacity(opacityValue)}/>`;
}

function diamond(size = 15, width = INNER_STROKE, opacityValue = 1): string {
  const half = size / 2;
  return polygon([[24, 24 - half], [24 + half, 24], [24, 24 + half], [24 - half, 24]], width, opacityValue);
}

function square(size = 14, width = INNER_STROKE, opacityValue = 1): string {
  const half = size / 2;
  return polygon([[24 - half, 24 - half], [24 + half, 24 - half], [24 + half, 24 + half], [24 - half, 24 + half]], width, opacityValue);
}

function hexagon(radius = 9.5, width = INNER_STROKE, opacityValue = 1): string {
  return polygon([0, 60, 120, 180, 240, 300].map((angle) => polar(radius, angle)), width, opacityValue);
}

function orbitDots(angles: number[], radius = 11, dotRadius = 1.85, opacityValue = 1): string[] {
  return angles.map((angle) => dot(angle, radius, dotRadius, opacityValue));
}

function horizontalStack(offsets: number[], length = 22, width = INNER_STROKE): string[] {
  return offsets.map((offset) => hline(offset, length, width));
}

function verticalStack(offsets: number[], length = 22, width = INNER_STROKE): string[] {
  return offsets.map((offset) => vline(offset, length, width));
}

function capsulePair(axis: "horizontal" | "vertical", offset = 4.8, length = 17, width = 3.2): string[] {
  if (axis === "horizontal") return [hline(-offset, length, width), hline(offset, length, width)];
  return [vline(-offset, length, width), vline(offset, length, width)];
}

function chevrons(direction: "up" | "down" | "left" | "right", width = INNER_STROKE): string[] {
  if (direction === "up") {
    return [shortLine(20, 27, 4, -4, width), shortLine(28, 27, -4, -4, width), shortLine(20, 19, 4, -4, width), shortLine(28, 19, -4, -4, width)];
  }
  if (direction === "down") {
    return [shortLine(20, 21, 4, 4, width), shortLine(28, 21, -4, 4, width), shortLine(20, 29, 4, 4, width), shortLine(28, 29, -4, 4, width)];
  }
  if (direction === "left") {
    return [shortLine(27, 20, -4, 4, width), shortLine(27, 28, -4, -4, width), shortLine(19, 20, -4, 4, width), shortLine(19, 28, -4, -4, width)];
  }
  return [shortLine(21, 20, 4, 4, width), shortLine(21, 28, 4, -4, width), shortLine(29, 20, 4, 4, width), shortLine(29, 28, 4, -4, width)];
}

function segmentedCore(segments: Array<[number, number]>, inner: string[]): string[] {
  return [...ringSegments(segments), ...inner];
}

function templates(): GlyphTemplate[] {
  const cardinal = [0, 90, 180, 270];
  const diagonal = [45, 135, 225, 315];
  const octants = [0, 45, 90, 135, 180, 225, 270, 315];
  const tri = [0, 120, 240];
  const six = [0, 60, 120, 180, 240, 300];
  const segmentedA: Array<[number, number]> = [[8, 76], [104, 172], [188, 256], [284, 352]];
  const segmentedB: Array<[number, number]> = [[20, 132], [200, 312]];
  const segmentedC: Array<[number, number]> = [[0, 48], [72, 120], [144, 192], [216, 264], [288, 336]];
  const segmentedD: Array<[number, number]> = [[38, 108], [142, 212], [252, 322]];
  const segmentedE: Array<[number, number]> = [[350, 58], [86, 154], [178, 246], [270, 338]];

  return [
    { name: "silence-ring", tags: ["minimal", "simple"], draw: () => [circle()] },
    { name: "vertical-mark", tags: ["minimal", "simple"], draw: () => [circle(), line(0, 27)] },
    { name: "horizontal-mark", tags: ["minimal", "simple"], draw: () => [circle(), line(90, 27)] },
    { name: "parallel-vertical-bars", tags: ["dashboard", "balanced", "filled-lines"], draw: () => [circle(), ...verticalStack([-5, 5], 21, 2.9)] },
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
    { name: "three-horizontal-bars", tags: ["dashboard", "dense", "filled-lines"], draw: () => [circle(), ...horizontalStack([-6.5, 0, 6.5], 22.5, 3.15)] },
    { name: "octant-dot-core", tags: ["mystic", "dense"], draw: () => [circle(), ...orbitDots(octants, 10.8, 1.62, 0.9), centerDot(1.85, 0.82)] },

    { name: "segmented-cardinal-bars", tags: ["premium-ui", "dashboard", "dense", "segmented-ring", "filled-lines"], draw: () => segmentedCore(segmentedA, verticalStack([-5.2, 5.2], 18.5, 2.9)) },
    { name: "segmented-horizontal-bars", tags: ["dashboard", "dense", "segmented-ring", "filled-lines"], draw: () => segmentedCore(segmentedA, horizontalStack([-5.2, 5.2], 18.5, 2.9)) },
    { name: "segmented-target-core", tags: ["premium-ui", "tech", "dense", "segmented-ring"], draw: () => segmentedCore(segmentedC, [circle(8.5, 2.5, 0.82), centerDot(2.45, 0.92)]) },
    { name: "segmented-diamond-core", tags: ["geometric", "dense", "segmented-ring"], draw: () => segmentedCore(segmentedB, [diamond(15, 3), centerDot(1.75, 0.82)]) },
    { name: "segmented-square-core", tags: ["geometric", "dashboard", "dense", "segmented-ring"], draw: () => segmentedCore(segmentedD, [square(13.5, 2.8), centerDot(2.1, 0.84)]) },
    { name: "segmented-hex-core", tags: ["geometric", "tech", "dense", "segmented-ring"], draw: () => segmentedCore(segmentedE, [hexagon(9.2, 2.7), centerDot(1.9, 0.85)]) },
    { name: "segmented-orbit-triad", tags: ["mystic", "dense", "segmented-ring"], draw: () => segmentedCore(segmentedD, [...orbitDots(tri, 10.8, 2.25), centerDot(1.7, 0.82)]) },
    { name: "segmented-orbit-six", tags: ["mystic", "dense", "segmented-ring"], draw: () => segmentedCore(segmentedC, [...orbitDots(six, 10.5, 1.65), centerDot(1.8, 0.82)]) },
    { name: "segmented-ladder", tags: ["dashboard", "dense", "segmented-ring", "filled-lines"], draw: () => segmentedCore(segmentedB, [...horizontalStack([-7, -2.3, 2.3, 7], 17.5, 2.35)]) },
    { name: "segmented-column-ladder", tags: ["dashboard", "dense", "segmented-ring", "filled-lines"], draw: () => segmentedCore(segmentedB, [...verticalStack([-7, -2.3, 2.3, 7], 17.5, 2.35)]) },
    { name: "segmented-capsule-pair", tags: ["premium-ui", "dense", "segmented-ring", "filled-lines"], draw: () => segmentedCore(segmentedA, capsulePair("horizontal", 4.8, 17, 3.15)) },
    { name: "segmented-vertical-capsules", tags: ["premium-ui", "dense", "segmented-ring", "filled-lines"], draw: () => segmentedCore(segmentedA, capsulePair("vertical", 4.8, 17, 3.15)) },
    { name: "segmented-nested-arcs", tags: ["organic", "dense", "segmented-ring"], draw: () => segmentedCore(segmentedE, [arc(320, 40, 3, 9.3), arc(140, 220, 3, 9.3), centerDot(1.9, 0.86)]) },
    { name: "segmented-offset-dots", tags: ["premium-ui", "dense", "segmented-ring"], draw: () => segmentedCore(segmentedD, [...orbitDots([30, 150, 210, 330], 10.4, 1.95), centerDot(2.1, 0.84)]) },
    { name: "segmented-core-band", tags: ["tech", "dashboard", "dense", "segmented-ring", "filled-lines"], draw: () => segmentedCore(segmentedC, [hline(0, 21, 3.6), hline(-5.6, 14, 2.35), hline(5.6, 14, 2.35)]) },

    { name: "filled-five-bars", tags: ["dashboard", "dense", "filled-lines"], draw: () => [circle(), ...horizontalStack([-8, -4, 0, 4, 8], 18, 2.05)] },
    { name: "filled-five-columns", tags: ["dashboard", "dense", "filled-lines"], draw: () => [circle(), ...verticalStack([-8, -4, 0, 4, 8], 18, 2.05)] },
    { name: "filled-broad-stack", tags: ["premium-ui", "dashboard", "dense", "filled-lines"], draw: () => [circle(), ...horizontalStack([-6.6, 0, 6.6], 24, 3.45)] },
    { name: "filled-column-stack", tags: ["premium-ui", "dashboard", "dense", "filled-lines"], draw: () => [circle(), ...verticalStack([-6.6, 0, 6.6], 24, 3.45)] },
    { name: "filled-thin-rhythm", tags: ["dashboard", "dense", "filled-lines"], draw: () => [circle(), hline(-8, 12, 2), hline(-4, 22, 2.15), hline(0, 16, 2.25), hline(4, 22, 2.15), hline(8, 12, 2)] },
    { name: "filled-vertical-rhythm", tags: ["dashboard", "dense", "filled-lines"], draw: () => [circle(), vline(-8, 12, 2), vline(-4, 22, 2.15), vline(0, 16, 2.25), vline(4, 22, 2.15), vline(8, 12, 2)] },
    { name: "filled-double-window", tags: ["dashboard", "balanced", "filled-lines"], draw: () => [circle(), hline(-5, 20, 3), hline(5, 20, 3), ...orbitDots([90, 270], 10, 2.1)] },
    { name: "filled-column-window", tags: ["dashboard", "balanced", "filled-lines"], draw: () => [circle(), vline(-5, 20, 3), vline(5, 20, 3), ...orbitDots([0, 180], 10, 2.1)] },
    { name: "filled-quiet-equalizer", tags: ["dashboard", "dense", "filled-lines"], draw: () => [circle(), vline(-7.2, 12, 2.6), vline(-2.4, 20, 2.6), vline(2.4, 16, 2.6), vline(7.2, 22, 2.6)] },
    { name: "filled-horizontal-equalizer", tags: ["dashboard", "dense", "filled-lines"], draw: () => [circle(), hline(-7.2, 12, 2.6), hline(-2.4, 20, 2.6), hline(2.4, 16, 2.6), hline(7.2, 22, 2.6)] },
    { name: "filled-chevrons-up", tags: ["tech", "dense", "filled-lines"], draw: () => [circle(), ...chevrons("up", 2.55)] },
    { name: "filled-chevrons-down", tags: ["tech", "dense", "filled-lines"], draw: () => [circle(), ...chevrons("down", 2.55)] },
    { name: "filled-chevrons-left", tags: ["tech", "dense", "filled-lines"], draw: () => [circle(), ...chevrons("left", 2.55)] },
    { name: "filled-chevrons-right", tags: ["tech", "dense", "filled-lines"], draw: () => [circle(), ...chevrons("right", 2.55)] },

    { name: "nested-double-halo", tags: ["premium-ui", "balanced"], draw: () => [circle(), circle(11.8, 2.6, 0.72), circle(6.5, 2.25, 0.68), centerDot(1.8, 0.82)] },
    { name: "nested-orbit-halo", tags: ["premium-ui", "dense"], draw: () => [circle(), circle(12, 2.25, 0.72), ...orbitDots(cardinal, 7.5, 1.8), centerDot(1.7, 0.82)] },
    { name: "inner-square-dots", tags: ["geometric", "dense"], draw: () => [circle(), square(14, 2.5), ...orbitDots(cardinal, 10.4, 1.8)] },
    { name: "inner-diamond-dots", tags: ["geometric", "dense"], draw: () => [circle(), diamond(15, 2.5), ...orbitDots(diagonal, 10.2, 1.7)] },
    { name: "hex-orbit-core", tags: ["geometric", "dense"], draw: () => [circle(), hexagon(9.5, 2.5), ...orbitDots(six, 12, 1.45, 0.88)] },
    { name: "triad-halo-core", tags: ["mystic", "balanced"], draw: () => [circle(), ...orbitDots(tri, 11.5, 2.4), circle(7, 2.2, 0.72)] },
    { name: "inverted-triad-halo", tags: ["mystic", "balanced"], draw: () => [circle(), ...orbitDots([60, 180, 300], 11.5, 2.4), circle(7, 2.2, 0.72)] },
    { name: "organic-petal-vertical", tags: ["organic", "dense"], draw: () => [circle(), arc(330, 30, 3.1, 12), arc(150, 210, 3.1, 12), arc(36, 144, 2.6, 7.8), arc(216, 324, 2.6, 7.8), centerDot(1.7, 0.82)] },
    { name: "organic-petal-horizontal", tags: ["organic", "dense"], draw: () => [circle(), arc(60, 120, 3.1, 12), arc(240, 300, 3.1, 12), arc(306, 54, 2.6, 7.8), arc(126, 234, 2.6, 7.8), centerDot(1.7, 0.82)] },
    { name: "organic-nested-crescents", tags: ["organic", "dense"], draw: () => [circle(), arc(300, 60, 3.1, 11.4), arc(120, 240, 3.1, 11.4), arc(320, 40, 2.2, 6.2), arc(140, 220, 2.2, 6.2), centerDot(1.65, 0.84)] },
    { name: "premium-soft-band", tags: ["premium-ui", "balanced", "filled-lines"], draw: () => [circle(), hline(0, 23, 4.2), ...orbitDots([0, 180], 9.8, 1.8, 0.85)] },
    { name: "premium-soft-column", tags: ["premium-ui", "balanced", "filled-lines"], draw: () => [circle(), vline(0, 23, 4.2), ...orbitDots([90, 270], 9.8, 1.8, 0.85)] },
    { name: "premium-inner-capsules", tags: ["premium-ui", "dense", "filled-lines"], draw: () => [circle(), ...capsulePair("horizontal", 5.8, 20, 2.85), hline(0, 11, 2.5)] },
    { name: "premium-inner-columns", tags: ["premium-ui", "dense", "filled-lines"], draw: () => [circle(), ...capsulePair("vertical", 5.8, 20, 2.85), vline(0, 11, 2.5)] },
    { name: "tech-orbit-bars", tags: ["tech", "dense", "filled-lines"], draw: () => [circle(), hline(-5.8, 19, 2.55), hline(5.8, 19, 2.55), ...orbitDots([0, 180], 10.5, 1.8)] },
    { name: "tech-column-bars", tags: ["tech", "dense", "filled-lines"], draw: () => [circle(), vline(-5.8, 19, 2.55), vline(5.8, 19, 2.55), ...orbitDots([90, 270], 10.5, 1.8)] },
    { name: "dashboard-four-pills", tags: ["dashboard", "dense", "filled-lines"], draw: () => [circle(), hline(-7, 15, 2.45), hline(-2.3, 21, 2.45), hline(2.3, 21, 2.45), hline(7, 15, 2.45)] },
    { name: "dashboard-four-columns", tags: ["dashboard", "dense", "filled-lines"], draw: () => [circle(), vline(-7, 15, 2.45), vline(-2.3, 21, 2.45), vline(2.3, 21, 2.45), vline(7, 15, 2.45)] },
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
  const segmented = base.filter((template) => template.tags.includes("segmented-ring") && !template.tags.includes(spec.style));
  const filledLines = base.filter((template) => template.tags.includes("filled-lines") && !template.tags.includes(spec.style) && !template.tags.includes("segmented-ring"));
  const rest = base.filter((template) => !template.tags.includes(spec.style) && !template.tags.includes("segmented-ring") && !template.tags.includes("filled-lines"));
  return [
    ...shuffle(styleMatches, `${spec.seed}|${spec.style}|style`),
    ...shuffle(segmented, `${spec.seed}|segmented`),
    ...shuffle(filledLines, `${spec.seed}|filled-lines`),
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
