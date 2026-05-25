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
4. writes one quality-gated SVG per glyph, preferring `potrace`/`vtracer` contour output when it survives the rendered-diff threshold and falling back to exact `lossless-runs` paths otherwise;
5. renders each SVG back to PNG;
6. writes final product PNGs at 500×500;
7. writes crop/render/diff artifacts and `manifest.json`;
8. writes `contact_sheet.png` for human review.

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

Current local batch result over readable files in `images/`:

```txt
readable packs: 33
generated glyphs: 3745
PNG export size: 500x500
missing artifacts: 0
bad PNG sizes: 0
minimum SSIM: 0.9850860531508355
mean SSIM: 0.9998556508395932
minimum foreground IoU: 0.9714285714285714
mean foreground IoU: 0.999892876396624
```

One local source fixture is corrupt/unreadable despite a `.jpg` extension and is recorded as `FAILED.txt` rather than blocking the whole batch.

## Quality philosophy

The tool should never claim success from browser redirects, raw file existence, or naive SVG export. Every SVG must be rendered back and compared to its source crop.

The acceptance standard is:

> visually identical to a human at the source resolution after monochrome normalization.

Default mode is quality-gated `auto`: try cleaner `potrace`/`vtracer` contour SVGs, render and score them, then use exact `lossless-runs` if a contour candidate would visibly damage fidelity. This gives a measurable quality anchor without embedding raster images. Later optimizer passes may produce cleaner curves/primitives, but only if they pass the same visual-diff gate.

## Future vectorizer.app stages

1. **Curation/filtering layer** — reject text fragments, watermarks, tiny blobs, clipped symbols, and low-value detections that are faithfully vectorized but not sellable glyphs.
2. **Primitive optimizer** — convert exact masks to cleaner path contours, circles, arcs, lines, triangles, and polygons where the visual diff remains invisible.
3. **Interactive review lab** — show source / crop / SVG render / diff / score and let the user reject or merge/split detections.
4. **Auto-grid and manual correction tools** — handle titles, captions, watermarks, repeated motifs, low contrast, tilted sheets, and mixed spacing.
5. **Pack builder** — rename, normalize viewBoxes, group, price, and export curated packs for VectorGlyphs.
6. **Optional model assistance** — use vision/LLM models for semantic naming, duplicate detection, weak-segmentation suggestions, and primitive-fitting hints, never as the sole source of truth; rendered diff remains the quality gate.
