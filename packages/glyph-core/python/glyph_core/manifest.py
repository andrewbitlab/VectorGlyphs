from __future__ import annotations

from typing import Any

from .specs import GlyphGenerationSpec, GlyphSet


def build_manifest(glyph_set: GlyphSet, spec: GlyphGenerationSpec) -> dict[str, Any]:
    return {
        "schemaVersion": 1,
        "generator": "vectorglyphs-glyph-core",
        "specHash": glyph_set.spec_hash,
        "spec": spec.to_dict(),
        "glyphs": [
            {
                "id": glyph.id,
                "name": glyph.name,
                "template": glyph.template,
                "tags": list(glyph.tags),
                "svgFile": f"{glyph.id}-{glyph.name}.svg",
                "viewBox": spec.view_box,
                "transparentBackground": spec.background is None and spec.palette.background is None,
            }
            for glyph in glyph_set.glyphs
        ],
    }
