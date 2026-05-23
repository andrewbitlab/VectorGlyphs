# glyph_core Python Package

Standalone deterministic procedural glyph generation core for VectorGlyphs.

## Implemented in Phase 1

- `GlyphGenerationSpec`, `Palette`, `Glyph`, and `GlyphSet` models.
- Seed/spec deterministic glyph-set generation.
- Refactored circular glyph templates derived from the original generator reference.
- Clean SVG rendering with `viewBox="0 0 48 48"`, no scripts, no external resources, and recolorable `currentColor` geometry.
- JSON-serializable manifest generation.
- Server-side PNG export helper for whitelisted sizes: `512`, `1024`, `2048`, `4096`.
- Pytest coverage for determinism, seed variation, metadata, SVG cleanliness, manifest shape, PNG dimensions, and validation.

## Development

```bash
cd packages/glyph-core/python
python -m venv .venv
.venv/bin/python -m pip install -e '.[dev]'
.venv/bin/python -m pytest -q
```

## Sample gallery

From the repository root:

```bash
packages/glyph-core/python/.venv/bin/python scripts/generate_sample_gallery.py \
  --count 6 \
  --seed phase-1-sample \
  --style premium-ui \
  --png-size 512
```

Outputs are written to:

```txt
packages/glyph-core/sample-gallery/phase1/
```
