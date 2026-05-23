# Vectorizer Core

`vectorizer-core` is the first internal implementation of the future `vectorizer.app` engine. It solves the immediate VectorGlyphs pivot problem: users upload monochrome icon/glyph sheets from the internet, the tool extracts individual symbols, converts each crop into SVG, renders the SVG back to PNG, and writes a measurable visual-diff report.

## Current scope

This first iteration is deliberately **monochrome-first**:

- black-on-light, white-on-dark, or tinted monochrome sources are normalized into a boolean ink mask;
- sheets are segmented into numbered glyph crops using foreground polarity detection, morphology, connected components, row/column reading order, and padding;
- each glyph is exported as SVG path data with no `<image>`, no scripts, and no external resources;
- default SVG mode is `lossless-runs`, a fidelity-first path representation that reproduces the normalized monochrome crop exactly at the source resolution;
- benchmark reports include original monochrome crop, rendered SVG PNG, amplified diff, scores, and contact sheet.

The quality target for this phase is: **difference not recognizable by a human after monochrome normalization at source resolution**. On the first benchmark sheet, the generated SVG renders match the normalized crops with `SSIM=1.0` and `foreground_iou=1.0`.

## Local setup

```bash
cd packages/vectorizer-core/python
python3 -m venv .venv
.venv/bin/python -m pip install -e '.[dev]'
.venv/bin/python -m pytest -q
```

## Run the benchmark

```bash
cd packages/vectorizer-core/python
.venv/bin/vectorizer-core \
  '/Users/andrzej/Projects/VectorGlyphs/images/46674448-outline-vector-icons-for-web-and-mobile-152-glyph.jpg' \
  --output-dir /Users/andrzej/Projects/VectorGlyphs/.tmp/vectorizer/46674448 \
  --max-glyphs 220
```

Outputs:

```txt
.tmp/vectorizer/46674448/manifest.json
.tmp/vectorizer/46674448/contact_sheet.png
.tmp/vectorizer/46674448/svg/glyph_001.svg ...
.tmp/vectorizer/46674448/render/glyph_001.png ...
.tmp/vectorizer/46674448/diff/glyph_001.png ...
```

## Important design note

`lossless-runs` is intentionally not the final prettiest SVG representation. It is the **quality anchor**: it proves segmentation, monochrome normalization, and SVG round-tripping can be visually perfect at source resolution without embedding rasters. The next production-grade step is a second-pass optimizer that converts these exact masks into cleaner semantic primitives/contours where it can do so without failing the visual-diff gate.

Future pipeline:

1. fidelity-first SVG from normalized mask;
2. primitive/contour simplification candidate;
3. render candidate;
4. compare against fidelity anchor;
5. accept simplification only if the diff remains human-invisible;
6. otherwise keep the exact path.
