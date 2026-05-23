from __future__ import annotations

from glyph_core import GlyphGenerationSpec, Palette, generate_glyph_set, render_svg

from app.schemas import GenerateRequest, GenerateResponse, GlyphPreview


def make_spec(request: GenerateRequest) -> GlyphGenerationSpec:
    return GlyphGenerationSpec(
        seed=request.seed,
        count=request.count,
        style=request.style,
        complexity=request.complexity,
        palette=Palette(stroke=request.stroke, background=request.background),
        background=request.background,
    )


def generate_preview_response(request: GenerateRequest) -> GenerateResponse:
    spec = make_spec(request)
    glyph_set = generate_glyph_set(spec)
    return GenerateResponse(
        specHash=glyph_set.spec_hash,
        glyphs=[
            GlyphPreview(
                id=glyph.id,
                name=glyph.name,
                template=glyph.template,
                tags=list(glyph.tags),
                svg=render_svg(glyph, spec),
            )
            for glyph in glyph_set.glyphs
        ],
    )
