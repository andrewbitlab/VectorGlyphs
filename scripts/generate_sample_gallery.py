#!/usr/bin/env python3
"""Generate a small local sample gallery for Phase 1 verification.

This script intentionally writes inside the VectorGlyphs repository only.
"""
from __future__ import annotations

import argparse
import json
import math
from pathlib import Path

from PIL import Image, ImageDraw

from glyph_core import GlyphGenerationSpec, Palette, export_png, generate_glyph_set, render_svg
from glyph_core.manifest import build_manifest


def generate_sample_gallery(out_dir: Path, count: int, seed: str, style: str, png_size: int) -> None:
    out_dir.mkdir(parents=True, exist_ok=True)
    for stale in [*out_dir.glob("*.svg"), *out_dir.glob("*.png"), out_dir / "manifest.json"]:
        if stale.exists():
            stale.unlink()

    spec = GlyphGenerationSpec(
        seed=seed,
        count=count,
        style=style,
        complexity="balanced",
        stroke_width=2.0,
        palette=Palette(stroke="#9d9788", background=None),
        background=None,
    )
    glyph_set = generate_glyph_set(spec)
    manifest = build_manifest(glyph_set, spec)

    png_paths: list[Path] = []
    for glyph in glyph_set.glyphs:
        svg = render_svg(glyph, spec)
        stem = f"{glyph.id}-{glyph.name}"
        (out_dir / f"{stem}.svg").write_text(svg, encoding="utf-8")
        png_path = out_dir / f"{stem}-{png_size}.png"
        png_path.write_bytes(export_png(svg, png_size))
        png_paths.append(png_path)

    cell = 176
    padding = 24
    cols = min(3, len(png_paths)) or 1
    rows = math.ceil(len(png_paths) / cols)
    sheet = Image.new("RGBA", (cols * cell + (cols + 1) * padding, rows * (cell + 34) + (rows + 1) * padding), "#050a08")
    draw = ImageDraw.Draw(sheet)
    for index, (glyph, png_path) in enumerate(zip(glyph_set.glyphs, png_paths, strict=True)):
        row, col = divmod(index, cols)
        x = padding + col * (cell + padding)
        y = padding + row * (cell + 34 + padding)
        draw.rounded_rectangle([x, y, x + cell, y + cell], radius=22, fill="#101713", outline="#31372f", width=1)
        glyph_image = Image.open(png_path).convert("RGBA").resize((cell, cell))
        sheet.alpha_composite(glyph_image, (x, y))
        draw.text((x + cell / 2, y + cell + 12), glyph.name, anchor="mt", fill="#f7f1df")
    sheet.save(out_dir / "contact-sheet.png")

    (out_dir / "manifest.json").write_text(json.dumps(manifest, indent=2, sort_keys=True), encoding="utf-8")
    (out_dir / "README.md").write_text(
        "# Phase 1 Sample Gallery\n\n"
        f"Generated from `glyph_core` with seed `{seed}`, style `{style}`, count `{count}`, "
        f"and PNG size `{png_size}`.\n",
        encoding="utf-8",
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", default="packages/glyph-core/sample-gallery/phase1")
    parser.add_argument("--count", type=int, default=6)
    parser.add_argument("--seed", default="phase-1-sample")
    parser.add_argument("--style", default="premium-ui")
    parser.add_argument("--png-size", type=int, default=512, choices=[512, 1024, 2048, 4096])
    args = parser.parse_args()

    generate_sample_gallery(Path(args.out), args.count, args.seed, args.style, args.png_size)
    print(f"Generated {args.count} glyphs in {args.out}")


if __name__ == "__main__":
    main()
