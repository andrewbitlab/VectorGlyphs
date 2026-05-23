# VectorGlyphs API

Phase 3 implements the local FastAPI export backend for glyph generation and file exports.

## Implemented endpoints

- `GET /health` — service health and version.
- `POST /api/generate` — deterministic glyph preview response with inline SVG.
- `POST /api/export` — local export bundle generation with SVG files, PNG files, `manifest.json`, and a ZIP archive.

## Local commands

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -e '.[dev]' -e ../../packages/glyph-core/python
.venv/bin/python -m pytest -q
.venv/bin/uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

Export artifacts are written under local ignored storage and are not payment-gated in Phase 3. Stripe/payment work starts in Phase 4 only.
