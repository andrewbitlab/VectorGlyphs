from __future__ import annotations

import argparse
import json
from pathlib import Path

from PIL import Image

from . import (
    SegmenterConfig,
    VectorizerConfig,
    compare_images,
    create_monochrome_mask,
    make_contact_sheet,
    mask_to_reference_image,
    render_svg_to_png,
    save_diff,
    segment_glyph_sheet,
    vectorize_mask_to_svg,
)


def run_vectorizer(input_path: Path, output_dir: Path, max_glyphs: int = 250) -> Path:
    input_path = Path(input_path)
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    svg_dir = output_dir / "svg"
    render_dir = output_dir / "render"
    crop_dir = output_dir / "crop"
    diff_dir = output_dir / "diff"
    for directory in [svg_dir, render_dir, crop_dir, diff_dir]:
        directory.mkdir(parents=True, exist_ok=True)

    image = Image.open(input_path).convert("RGB")
    mask = create_monochrome_mask(image)
    glyphs = segment_glyph_sheet(image, mask, SegmenterConfig(max_glyphs=max_glyphs))
    manifest_glyphs: list[dict[str, object]] = []
    manifest: dict[str, object] = {
        "input": str(input_path),
        "output_dir": str(output_dir),
        "source_size": {"width": image.width, "height": image.height},
        "mode": "monochrome-first-pass",
        "glyphs": manifest_glyphs,
    }
    contact_rows = []

    for glyph in glyphs:
        stem = f"glyph_{glyph.index:03d}"
        svg = vectorize_mask_to_svg(glyph.mask, VectorizerConfig(stroke_color="#000000", simplify_tolerance=0.35))
        render = render_svg_to_png(svg, glyph.mask.shape[1], glyph.mask.shape[0])
        reference = mask_to_reference_image(glyph.mask)
        score = compare_images(reference, render)

        crop_path = crop_dir / f"{stem}.png"
        svg_path = svg_dir / f"{stem}.svg"
        render_path = render_dir / f"{stem}.png"
        diff_path = diff_dir / f"{stem}.png"
        reference.save(crop_path)
        svg_path.write_text(svg, encoding="utf-8")
        render.save(render_path)
        save_diff(reference, render, diff_path)
        contact_rows.append((f"{glyph.index:03d} ssim={score.ssim:.4f}", reference, render, Image.open(diff_path)))
        manifest_glyphs.append(
            {
                "index": glyph.index,
                "bbox": glyph.bbox.to_dict(),
                "foreground_pixels": glyph.foreground_pixels,
                "crop_path": str(crop_path),
                "svg_path": str(svg_path),
                "render_path": str(render_path),
                "diff_path": str(diff_path),
                "score": score.to_dict(),
            }
        )

    make_contact_sheet(contact_rows, output_dir / "contact_sheet.png")
    manifest_path = output_dir / "manifest.json"
    manifest_path.write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    return manifest_path


def main() -> None:
    parser = argparse.ArgumentParser(description="Extract monochrome icon sheets into SVG glyphs.")
    parser.add_argument("input_path", type=Path)
    parser.add_argument("--output-dir", type=Path, default=Path("outputs/vectorizer"))
    parser.add_argument("--max-glyphs", type=int, default=250)
    args = parser.parse_args()
    manifest_path = run_vectorizer(args.input_path, args.output_dir, args.max_glyphs)
    print(manifest_path)


if __name__ == "__main__":
    main()
