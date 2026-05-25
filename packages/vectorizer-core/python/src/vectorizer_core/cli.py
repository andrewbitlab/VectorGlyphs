from __future__ import annotations

import argparse
import json
import re
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
    render_svg_to_product_png,
    save_diff,
    segment_glyph_sheet,
    trace_mask_to_svg_best_effort,
)

SUPPORTED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".avif", ".webp", ".bmp", ".tif", ".tiff"}


def slugify_name(name: str) -> str:
    stem = Path(name).stem
    slug = re.sub(r"[^A-Za-z0-9]+", "-", stem).strip("-").lower()
    return slug[:80] or "glyph-sheet"


def run_vectorizer(
    input_path: Path,
    output_dir: Path,
    max_glyphs: int = 250,
    *,
    png_size: int = 500,
    backend: str = "auto",
) -> Path:
    input_path = Path(input_path)
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    svg_dir = output_dir / "svg"
    render_dir = output_dir / "render"
    crop_dir = output_dir / "crop"
    diff_dir = output_dir / "diff"
    png_dir = output_dir / f"png-{png_size}"
    for directory in [svg_dir, render_dir, crop_dir, diff_dir, png_dir]:
        directory.mkdir(parents=True, exist_ok=True)

    image = Image.open(input_path).convert("RGB")
    mask = create_monochrome_mask(image)
    glyphs = segment_glyph_sheet(image, mask, SegmenterConfig(max_glyphs=max_glyphs))
    manifest_glyphs: list[dict[str, object]] = []
    manifest: dict[str, object] = {
        "input": str(input_path),
        "output_dir": str(output_dir),
        "source_size": {"width": image.width, "height": image.height},
        "mode": "monochrome-potrace-quality-gated",
        "preferred_backend": backend,
        "png_size": png_size,
        "glyphs": manifest_glyphs,
    }
    contact_rows = []

    for glyph in glyphs:
        stem = f"glyph_{glyph.index:03d}"
        result = trace_mask_to_svg_best_effort(
            glyph.mask,
            VectorizerConfig(stroke_color="#000000", simplify_tolerance=0.35),
            preferred_backend=backend,
        )
        svg = result.svg
        render = render_svg_to_png(svg, glyph.mask.shape[1], glyph.mask.shape[0])
        reference = mask_to_reference_image(glyph.mask)
        score = compare_images(reference, render)
        product_png = render_svg_to_product_png(
            svg,
            size=png_size,
            source_width=glyph.mask.shape[1],
            source_height=glyph.mask.shape[0],
        )

        crop_path = crop_dir / f"{stem}.png"
        svg_path = svg_dir / f"{stem}.svg"
        render_path = render_dir / f"{stem}.png"
        png_500_path = png_dir / f"{stem}.png"
        diff_path = diff_dir / f"{stem}.png"
        reference.save(crop_path)
        svg_path.write_text(svg, encoding="utf-8")
        render.save(render_path)
        product_png.save(png_500_path)
        save_diff(reference, render, diff_path)
        contact_rows.append((f"{glyph.index:03d} {result.backend} ssim={score.ssim:.4f}", reference, render, Image.open(diff_path)))
        manifest_glyphs.append(
            {
                "index": glyph.index,
                "backend": result.backend,
                "backend_score": result.score.to_dict(),
                "bbox": glyph.bbox.to_dict(),
                "foreground_pixels": glyph.foreground_pixels,
                "crop_path": str(crop_path),
                "svg_path": str(svg_path),
                "render_path": str(render_path),
                "png_500_path": str(png_500_path),
                "diff_path": str(diff_path),
                "score": score.to_dict(),
            }
        )

    make_contact_sheet(contact_rows, output_dir / "contact_sheet.png")
    manifest_path = output_dir / "manifest.json"
    manifest_path.write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    return manifest_path


def run_vectorizer_batch(
    input_dir: Path,
    output_dir: Path,
    *,
    max_glyphs: int = 350,
    png_size: int = 500,
    backend: str = "auto",
) -> list[Path]:
    input_dir = Path(input_dir)
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    manifests: list[Path] = []
    used_slugs: set[str] = set()
    for input_path in sorted(path for path in input_dir.iterdir() if path.is_file() and (path.suffix.lower() in SUPPORTED_EXTENSIONS or not path.suffix)):
        base_slug = slugify_name(input_path.name)
        slug = base_slug
        suffix = 2
        while slug in used_slugs:
            slug = f"{base_slug}-{suffix}"
            suffix += 1
        used_slugs.add(slug)
        try:
            manifests.append(run_vectorizer(input_path, output_dir / slug, max_glyphs=max_glyphs, png_size=png_size, backend=backend))
        except Exception as exc:
            failed_dir = output_dir / slug
            failed_dir.mkdir(parents=True, exist_ok=True)
            (failed_dir / "FAILED.txt").write_text(f"{type(exc).__name__}: {exc}\n", encoding="utf-8")
    return manifests


def main() -> None:
    parser = argparse.ArgumentParser(description="Extract monochrome icon sheets into SVG glyphs and transparent PNG exports.")
    parser.add_argument("input_path", type=Path, help="Image file or directory containing source images")
    parser.add_argument("--output-dir", type=Path, default=Path("outputs/vectorizer"))
    parser.add_argument("--max-glyphs", type=int, default=350)
    parser.add_argument("--png-size", type=int, default=500)
    parser.add_argument("--backend", choices=["auto", "potrace", "vtracer", "contour", "lossless-runs"], default="auto")
    args = parser.parse_args()
    if args.input_path.is_dir():
        manifests = run_vectorizer_batch(args.input_path, args.output_dir, max_glyphs=args.max_glyphs, png_size=args.png_size, backend=args.backend)
        for manifest_path in manifests:
            print(manifest_path)
    else:
        manifest_path = run_vectorizer(args.input_path, args.output_dir, args.max_glyphs, png_size=args.png_size, backend=args.backend)
        print(manifest_path)


if __name__ == "__main__":
    main()
