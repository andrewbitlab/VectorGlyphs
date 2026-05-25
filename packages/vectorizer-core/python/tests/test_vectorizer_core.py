from __future__ import annotations

import json
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw

from vectorizer_core import (
    SegmenterConfig,
    VectorizerConfig,
    compare_images,
    create_monochrome_mask,
    render_svg_to_product_png,
    render_svg_to_png,
    segment_glyph_sheet,
    trace_mask_to_svg_best_effort,
    vectorize_mask_to_svg,
)
from vectorizer_core.cli import run_vectorizer, run_vectorizer_batch


def _synthetic_sheet() -> Image.Image:
    image = Image.new("RGB", (360, 240), "white")
    draw = ImageDraw.Draw(image)
    cells = []
    for row in range(2):
        for col in range(3):
            x0 = 30 + col * 110
            y0 = 28 + row * 96
            cells.append((x0, y0, x0 + 64, y0 + 64))

    # Multi-component glyphs: circle + line, triangle + dot, outline square, etc.
    draw.ellipse(cells[0], outline="black", width=5)
    draw.line((cells[0][0] + 32, cells[0][1] + 12, cells[0][0] + 32, cells[0][3] - 12), fill="black", width=5)
    draw.polygon([(cells[1][0] + 32, cells[1][1] + 4), (cells[1][0] + 6, cells[1][3] - 8), (cells[1][2] - 6, cells[1][3] - 8)], outline="black")
    draw.ellipse((cells[1][0] + 28, cells[1][1] + 30, cells[1][0] + 36, cells[1][1] + 38), fill="black")
    draw.rectangle(cells[2], outline="black", width=5)
    draw.line((cells[2][0] + 14, cells[2][1] + 32, cells[2][2] - 14, cells[2][1] + 32), fill="black", width=5)
    draw.line((cells[3][0] + 12, cells[3][1] + 12, cells[3][2] - 12, cells[3][3] - 12), fill="black", width=6)
    draw.line((cells[3][2] - 12, cells[3][1] + 12, cells[3][0] + 12, cells[3][3] - 12), fill="black", width=6)
    for offset in (12, 24, 36, 48):
        draw.line((cells[4][0] + 10, cells[4][1] + offset, cells[4][2] - 10, cells[4][1] + offset), fill="black", width=4)
    draw.ellipse(cells[5], fill="black")
    draw.ellipse((cells[5][0] + 18, cells[5][1] + 18, cells[5][2] - 18, cells[5][3] - 18), fill="white")
    return image


def test_monochrome_mask_detects_foreground_on_light_and_dark_backgrounds() -> None:
    light = Image.new("RGB", (80, 80), "white")
    ImageDraw.Draw(light).rectangle((20, 20, 60, 60), fill="black")
    dark = Image.new("RGB", (80, 80), "black")
    ImageDraw.Draw(dark).rectangle((20, 20, 60, 60), fill="white")

    light_mask = create_monochrome_mask(light)
    dark_mask = create_monochrome_mask(dark)

    assert light_mask[40, 40]
    assert dark_mask[40, 40]
    assert not light_mask[5, 5]
    assert not dark_mask[5, 5]


def test_segments_sheet_into_numbered_glyph_crops_with_multicomponent_icons() -> None:
    sheet = _synthetic_sheet()
    mask = create_monochrome_mask(sheet)

    glyphs = segment_glyph_sheet(sheet, mask, SegmenterConfig(min_area_ratio=0.0008, max_glyphs=12))

    assert len(glyphs) == 6
    assert [glyph.index for glyph in glyphs] == [1, 2, 3, 4, 5, 6]
    assert glyphs[0].bbox.left < glyphs[1].bbox.left < glyphs[2].bbox.left
    assert glyphs[0].bbox.top < glyphs[3].bbox.top
    assert all(glyph.mask.any() for glyph in glyphs)


def test_vectorized_svg_renders_visually_identical_to_monochrome_crop() -> None:
    sheet = _synthetic_sheet()
    mask = create_monochrome_mask(sheet)
    glyph = segment_glyph_sheet(sheet, mask, SegmenterConfig(min_area_ratio=0.0008, max_glyphs=12))[0]

    svg = vectorize_mask_to_svg(glyph.mask, VectorizerConfig(stroke_color="#000000", simplify_tolerance=0.35))
    rendered = render_svg_to_png(svg, glyph.mask.shape[1], glyph.mask.shape[0])
    score = compare_images(Image.fromarray((~glyph.mask * 255).astype("uint8"), "L"), rendered)

    assert "<svg" in svg
    assert "<image" not in svg.lower()
    assert "<script" not in svg.lower()
    assert score.ssim >= 0.985
    assert score.foreground_iou >= 0.97


def test_best_effort_vectorizer_uses_potrace_when_quality_gate_passes() -> None:
    sheet = _synthetic_sheet()
    mask = create_monochrome_mask(sheet)
    glyph = segment_glyph_sheet(sheet, mask, SegmenterConfig(min_area_ratio=0.0008, max_glyphs=12))[0]

    result = trace_mask_to_svg_best_effort(glyph.mask, preferred_backend="potrace", min_ssim=0.75, min_iou=0.75)
    rendered = render_svg_to_png(result.svg, glyph.mask.shape[1], glyph.mask.shape[0])
    reference = Image.fromarray((~glyph.mask * 255).astype("uint8"), "L")
    score = compare_images(reference, rendered)

    assert result.backend in {"potrace", "lossless-runs"}
    assert "<image" not in result.svg.lower()
    assert "<!doctype" not in result.svg.lower()
    assert score.ssim >= 0.75


def test_product_png_export_is_500_square_from_svg_vector() -> None:
    sheet = _synthetic_sheet()
    mask = create_monochrome_mask(sheet)
    glyph = segment_glyph_sheet(sheet, mask, SegmenterConfig(min_area_ratio=0.0008, max_glyphs=12))[0]
    result = trace_mask_to_svg_best_effort(glyph.mask, preferred_backend="auto")

    png = render_svg_to_product_png(result.svg, size=500)

    assert png.size == (500, 500)
    assert png.mode == "RGBA"
    alpha = np.asarray(png.getchannel("A"))
    assert alpha.max() > 0


def test_cli_generates_manifest_svgs_renders_diffs_and_contact_sheet(tmp_path: Path) -> None:
    input_path = tmp_path / "sheet.png"
    out_dir = tmp_path / "out"
    _synthetic_sheet().save(input_path)

    manifest_path = run_vectorizer(input_path=input_path, output_dir=out_dir, max_glyphs=12)

    manifest = json.loads(manifest_path.read_text())
    assert manifest["input"].endswith("sheet.png")
    assert len(manifest["glyphs"]) == 6
    assert (out_dir / "contact_sheet.png").exists()
    for glyph in manifest["glyphs"]:
        assert Path(glyph["svg_path"]).exists()
        assert Path(glyph["render_path"]).exists()
        assert Path(glyph["png_500_path"]).exists()
        assert Image.open(glyph["png_500_path"]).size == (500, 500)
        assert Path(glyph["diff_path"]).exists()
        assert glyph["backend"] in {"potrace", "vtracer", "lossless-runs", "contour"}
        assert glyph["score"]["ssim"] >= 0.985


def test_batch_vectorizer_creates_one_output_folder_per_source_image(tmp_path: Path) -> None:
    input_dir = tmp_path / "images"
    input_dir.mkdir()
    _synthetic_sheet().save(input_dir / "sheet one.png")
    _synthetic_sheet().save(input_dir / "sheet-two.jpg")
    _synthetic_sheet().save(input_dir / "collision-2.png")
    _synthetic_sheet().save(input_dir / "collision.png")
    _synthetic_sheet().save(input_dir / "collision@.png")

    manifests = run_vectorizer_batch(input_dir=input_dir, output_dir=tmp_path / "packs", max_glyphs=12, png_size=500)

    assert len(manifests) == 5
    assert (tmp_path / "packs" / "sheet-one" / "png-500").exists()
    assert (tmp_path / "packs" / "sheet-two" / "png-500").exists()
    assert (tmp_path / "packs" / "collision" / "png-500").exists()
    assert (tmp_path / "packs" / "collision-2" / "png-500").exists()
    assert (tmp_path / "packs" / "collision-3" / "png-500").exists()
    assert len({manifest.parent.name for manifest in manifests}) == len(manifests)
