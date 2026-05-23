from __future__ import annotations

import json
import struct
import xml.etree.ElementTree as ET

from glyph_core import (
    GlyphGenerationSpec,
    Palette,
    export_png,
    generate_glyph_set,
    render_svg,
)
from glyph_core.manifest import build_manifest


def png_dimensions(data: bytes) -> tuple[int, int]:
    assert data.startswith(b"\x89PNG\r\n\x1a\n")
    return struct.unpack(">II", data[16:24])


def base_spec(**overrides) -> GlyphGenerationSpec:
    values = {
        "seed": "phase-1-seed",
        "count": 4,
        "style": "premium-ui",
        "complexity": "balanced",
        "stroke_width": 2.0,
        "palette": Palette(stroke="#9d9788", background=None),
        "view_box": "0 0 48 48",
    }
    values.update(overrides)
    return GlyphGenerationSpec(**values)


def test_generation_is_deterministic_for_same_seed_and_spec():
    spec = base_spec()

    first = generate_glyph_set(spec)
    second = generate_glyph_set(spec)

    assert [glyph.id for glyph in first.glyphs] == [glyph.id for glyph in second.glyphs]
    assert [glyph.name for glyph in first.glyphs] == [glyph.name for glyph in second.glyphs]
    assert [render_svg(glyph, spec) for glyph in first.glyphs] == [
        render_svg(glyph, spec) for glyph in second.glyphs
    ]


def test_different_seeds_generate_different_svg_output():
    first_spec = base_spec(seed="seed-a")
    second_spec = base_spec(seed="seed-b")

    first_svg = render_svg(generate_glyph_set(first_spec).glyphs[0], first_spec)
    second_svg = render_svg(generate_glyph_set(second_spec).glyphs[0], second_spec)

    assert first_svg != second_svg


def test_generated_set_contains_expected_count_and_stable_metadata():
    spec = base_spec(seed="metadata-seed", count=6, style="tech", complexity="dense")

    glyph_set = generate_glyph_set(spec)

    assert glyph_set.spec_hash.startswith("sha256:")
    assert len(glyph_set.glyphs) == 6
    assert [glyph.id for glyph in glyph_set.glyphs] == [
        "glyph_001",
        "glyph_002",
        "glyph_003",
        "glyph_004",
        "glyph_005",
        "glyph_006",
    ]
    assert all(glyph.name for glyph in glyph_set.glyphs)


def test_rendered_svg_is_valid_clean_scalable_and_recolorable():
    spec = base_spec(seed="svg-clean", count=1)
    glyph = generate_glyph_set(spec).glyphs[0]

    svg = render_svg(glyph, spec)
    root = ET.fromstring(svg)

    assert root.tag.endswith("svg")
    assert root.attrib["viewBox"] == "0 0 48 48"
    assert root.attrib["role"] == "img"
    assert "<script" not in svg.lower()
    assert "href=" not in svg.lower()
    assert "xlink:href" not in svg.lower()
    assert "https://" not in svg.lower()
    assert "currentColor" in svg
    assert "<rect" not in svg


def test_background_mode_adds_background_rect_only_when_requested():
    transparent_spec = base_spec(seed="background", background=None, palette=Palette(stroke="#ffffff", background=None))
    filled_spec = base_spec(seed="background", background="#111827", palette=Palette(stroke="#ffffff", background="#111827"))

    transparent_svg = render_svg(generate_glyph_set(transparent_spec).glyphs[0], transparent_spec)
    filled_svg = render_svg(generate_glyph_set(filled_spec).glyphs[0], filled_spec)

    assert "<rect" not in transparent_svg
    assert "<rect" in filled_svg
    assert "#111827" in filled_svg


def test_manifest_is_json_serializable_and_describes_glyphs():
    spec = base_spec(seed="manifest", count=2, style="geometric")
    glyph_set = generate_glyph_set(spec)

    manifest = build_manifest(glyph_set, spec)
    encoded = json.dumps(manifest, sort_keys=True)
    decoded = json.loads(encoded)

    assert decoded["schemaVersion"] == 1
    assert decoded["spec"]["seed"] == "manifest"
    assert decoded["spec"]["style"] == "geometric"
    assert decoded["specHash"] == glyph_set.spec_hash
    assert [glyph["id"] for glyph in decoded["glyphs"]] == ["glyph_001", "glyph_002"]


def test_png_export_returns_requested_dimensions():
    spec = base_spec(seed="png", count=1, background="#ffffff", palette=Palette(stroke="#111827", background="#ffffff"))
    svg = render_svg(generate_glyph_set(spec).glyphs[0], spec)

    png = export_png(svg, size=512, background="#ffffff")

    assert png_dimensions(png) == (512, 512)


def test_spec_validates_whitelisted_values_and_limits():
    try:
        base_spec(style="unsupported")
    except ValueError as error:
        assert "style" in str(error)
    else:
        raise AssertionError("unsupported style should fail validation")

    try:
        base_spec(count=1000)
    except ValueError as error:
        assert "count" in str(error)
    else:
        raise AssertionError("oversized count should fail validation")

    try:
        base_spec(palette=Palette(stroke="not-a-color", background=None))
    except ValueError as error:
        assert "color" in str(error).lower()
    else:
        raise AssertionError("invalid color should fail validation")
