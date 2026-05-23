from __future__ import annotations

import html
from collections.abc import Iterable

from .specs import Glyph, GlyphGenerationSpec


def _background_for(spec: GlyphGenerationSpec) -> str | None:
    return spec.background if spec.background is not None else spec.palette.background


def render_svg(glyph: Glyph, spec: GlyphGenerationSpec) -> str:
    background = _background_for(spec)
    background_element = ""
    if background is not None:
        background_element = f'  <rect width="48" height="48" rx="0" fill="{html.escape(background)}"/>\n'
    body = "\n    ".join(glyph.elements)
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" '
        f'viewBox="{html.escape(spec.view_box)}" role="img" aria-label="{html.escape(glyph.name)}" '
        f'color="{html.escape(spec.palette.stroke)}">\n'
        f'{background_element}'
        f'  <g id="glyph-{html.escape(glyph.id)}" data-name="{html.escape(glyph.name)}" '
        f'vector-effect="non-scaling-stroke">\n'
        f'    {body}\n'
        f'  </g>\n'
        f'</svg>\n'
    )


def render_svg_documents(glyphs: Iterable[Glyph], spec: GlyphGenerationSpec) -> dict[str, str]:
    return {glyph.id: render_svg(glyph, spec) for glyph in glyphs}
