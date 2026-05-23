# Vectorizer.app Pivot Plan

VectorGlyphs is pivoting from a primarily random glyph generator into a product that sells curated, ready-made glyph packs. The internal tool powering that pivot is the future `vectorizer.app`: a high-quality monochrome icon-sheet extraction and SVG vectorization workflow.

## Product problem

A user has an image downloaded from the web: a JPG/PNG/AVIF containing many monochrome icons, tattoo glyphs, esoteric symbols, alchemy marks, geometric shapes, UI glyphs, or logo-like elements. The user wants individual, clean SVG files without manually cropping and tracing every symbol.

## First implementation scope

Implemented now under:

```txt
packages/vectorizer-core/python
```

The first version:

1. loads a source image;
2. converts it to a monochrome foreground mask;
3. segments likely individual glyphs in reading order;
4. writes one SVG per glyph;
5. renders each SVG back to PNG;
6. writes crop/render/diff artifacts and `manifest.json`;
7. writes `contact_sheet.png` for human review.

The first mandatory benchmark is:

```txt
images/46674448-outline-vector-icons-for-web-and-mobile-152-glyph.jpg
```

Current result on that benchmark:

```txt
glyphs: 152
normalized-crop SSIM: min 1.0 / mean 1.0 / max 1.0
foreground IoU: min 1.0 / mean 1.0 / max 1.0
```

This score is against the normalized monochrome crop, not the noisy JPG background. That matches the agreed first-iteration scope: monochrome conversion is part of the edit/vectorization process.

## Quality philosophy

The tool should never claim success from browser redirects, raw file existence, or naive SVG export. Every SVG must be rendered back and compared to its source crop.

The acceptance standard is:

> visually identical to a human at the source resolution after monochrome normalization.

Default mode is fidelity-first `lossless-runs`: SVG path rectangles generated from the exact normalized ink mask. This gives a perfect quality anchor without embedding raster images. Later optimizer passes may produce cleaner curves/primitives, but only if they pass the same visual-diff gate.

## Future vectorizer.app stages

1. **Primitive optimizer** — convert exact masks to cleaner path contours, circles, arcs, lines, triangles, and polygons where the visual diff remains invisible.
2. **Interactive review lab** — show source / crop / SVG render / diff / score and let the user reject or merge/split detections.
3. **Auto-grid and manual correction tools** — handle titles, captions, watermarks, repeated motifs, low contrast, tilted sheets, and mixed spacing.
4. **Pack builder** — rename, normalize viewBoxes, group, price, and export curated packs for VectorGlyphs.
5. **Optional model assistance** — use vision/LLM models for semantic naming, duplicate detection, weak-segmentation suggestions, and primitive-fitting hints, never as the sole source of truth; rendered diff remains the quality gate.
