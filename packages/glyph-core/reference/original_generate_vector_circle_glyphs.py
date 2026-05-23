#!/usr/bin/env python3
"""Generate high-legibility quiet-luxury circular glyphs as pure SVG vectors.

Rules enforced by this generator:
- individual SVG files contain ONLY the glyph geometry on a transparent background;
- every glyph keeps one shared outer diameter / circular family language;
- differences are silhouette-first: bars, broken arcs, dots, rings, and simple inner marks
  stay readable at the real 24pt SwiftUI size;
- variant 00 is reserved for Silence: a plain empty ring.

Usage:
  python3 tools/generate_vector_circle_glyphs.py --count 24
  python3 tools/generate_vector_circle_glyphs.py --count 24 --selected --out tools/generated_vector_circle_glyphs_selected_v2
"""
from __future__ import annotations

import argparse
import json
import math
from dataclasses import dataclass
from pathlib import Path
from typing import Callable, Iterable

VIEWBOX = 48
CENTER = 24.0
RADIUS = 17.6
STROKE = 3.6
INNER_STROKE = 2.65
BOLD_STROKE = 4.35
MUTED = "#9d9788"
GOLD = "#d4b866"
PREVIEW_BG = "#050a08"
PREVIEW_CARD = "#101713"
PREVIEW_CARD_STROKE = "#31372f"


def fmt(value: float) -> str:
    text = f"{value:.4f}".rstrip("0").rstrip(".")
    return text if text != "-0" else "0"


def polar(cx: float, cy: float, r: float, angle_deg: float) -> tuple[float, float]:
    # 0° at 12 o'clock, clockwise-positive.
    angle = math.radians(angle_deg - 90)
    return cx + r * math.cos(angle), cy + r * math.sin(angle)


def opacity_attr(opacity: float) -> str:
    return f' opacity="{fmt(opacity)}"' if opacity != 1 else ""


def arc_path(start_deg: float, end_deg: float, r: float = RADIUS, cx: float = CENTER, cy: float = CENTER) -> str:
    span = (end_deg - start_deg) % 360
    if span == 0:
        span = 359.999
    sx, sy = polar(cx, cy, r, start_deg)
    ex, ey = polar(cx, cy, r, start_deg + span)
    large_arc = 1 if span > 180 else 0
    return f"M {fmt(sx)} {fmt(sy)} A {fmt(r)} {fmt(r)} 0 {large_arc} 1 {fmt(ex)} {fmt(ey)}"


def circle(r: float = RADIUS, stroke: str = MUTED, width: float = STROKE, opacity: float = 1.0) -> str:
    return (
        f'<circle cx="{fmt(CENTER)}" cy="{fmt(CENTER)}" r="{fmt(r)}" '
        f'fill="none" stroke="{stroke}" stroke-width="{fmt(width)}" '
        f'stroke-linecap="round" stroke-linejoin="round"{opacity_attr(opacity)}/>'
    )


def arc(start: float, end: float, stroke: str = MUTED, width: float = STROKE, r: float = RADIUS, opacity: float = 1.0) -> str:
    return (
        f'<path d="{arc_path(start, end, r)}" fill="none" stroke="{stroke}" '
        f'stroke-width="{fmt(width)}" stroke-linecap="round" stroke-linejoin="round"{opacity_attr(opacity)}/>'
    )


def line(angle: float, length: float, stroke: str = MUTED, width: float = BOLD_STROKE, opacity: float = 1.0) -> str:
    x1, y1 = polar(CENTER, CENTER, length / 2, angle)
    x2, y2 = polar(CENTER, CENTER, length / 2, angle + 180)
    return (
        f'<line x1="{fmt(x1)}" y1="{fmt(y1)}" x2="{fmt(x2)}" y2="{fmt(y2)}" '
        f'stroke="{stroke}" stroke-width="{fmt(width)}" stroke-linecap="round"{opacity_attr(opacity)}/>'
    )


def hline(y_offset: float, length: float, stroke: str = MUTED, width: float = INNER_STROKE, opacity: float = 1.0) -> str:
    y = CENTER + y_offset
    return (
        f'<line x1="{fmt(CENTER - length / 2)}" y1="{fmt(y)}" x2="{fmt(CENTER + length / 2)}" y2="{fmt(y)}" '
        f'stroke="{stroke}" stroke-width="{fmt(width)}" stroke-linecap="round"{opacity_attr(opacity)}/>'
    )


def vline(x_offset: float, length: float, stroke: str = MUTED, width: float = INNER_STROKE, opacity: float = 1.0) -> str:
    x = CENTER + x_offset
    return (
        f'<line x1="{fmt(x)}" y1="{fmt(CENTER - length / 2)}" x2="{fmt(x)}" y2="{fmt(CENTER + length / 2)}" '
        f'stroke="{stroke}" stroke-width="{fmt(width)}" stroke-linecap="round"{opacity_attr(opacity)}/>'
    )


def dot(angle: float, radius_from_center: float = RADIUS, dot_radius: float = 2.0, fill: str = MUTED, opacity: float = 1.0) -> str:
    x, y = polar(CENTER, CENTER, radius_from_center, angle)
    return f'<circle cx="{fmt(x)}" cy="{fmt(y)}" r="{fmt(dot_radius)}" fill="{fill}"{opacity_attr(opacity)}/>'


def center_dot(fill: str = MUTED, radius: float = 3.0, opacity: float = 1.0) -> str:
    return f'<circle cx="{fmt(CENTER)}" cy="{fmt(CENTER)}" r="{fmt(radius)}" fill="{fill}"{opacity_attr(opacity)}/>'


def diamond(stroke: str = MUTED, size: float = 15.0, width: float = INNER_STROKE, opacity: float = 1.0) -> str:
    half = size / 2
    points = [(CENTER, CENTER - half), (CENTER + half, CENTER), (CENTER, CENTER + half), (CENTER - half, CENTER)]
    d = "M " + " L ".join(f"{fmt(x)} {fmt(y)}" for x, y in points) + " Z"
    return (
        f'<path d="{d}" fill="none" stroke="{stroke}" stroke-width="{fmt(width)}" '
        f'stroke-linecap="round" stroke-linejoin="round"{opacity_attr(opacity)}/>'
    )


def orbit_dots(angles: Iterable[float], radius: float = RADIUS, dot_radius: float = 1.85, fill: str = MUTED, opacity: float = 1.0) -> list[str]:
    return [dot(angle, radius_from_center=radius, dot_radius=dot_radius, fill=fill, opacity=opacity) for angle in angles]


def symmetric_segments(centers: Iterable[float], span: float, stroke: str = MUTED, width: float = STROKE, r: float = RADIUS, opacity: float = 1.0) -> list[str]:
    half = span / 2
    return [arc(center - half, center + half, stroke=stroke, width=width, r=r, opacity=opacity) for center in centers]


@dataclass(frozen=True)
class GlyphSpec:
    name: str
    draw: Callable[[str], list[str]]


def glyphs() -> list[GlyphSpec]:
    cardinal = [0, 90, 180, 270]
    diagonal = [45, 135, 225, 315]
    octants = [0, 45, 90, 135, 180, 225, 270, 315]

    return [
        GlyphSpec("silence-ring", lambda c: [circle(stroke=c)]),
        GlyphSpec("vertical-mark", lambda c: [circle(stroke=c), line(0, 27.0, stroke=c, width=BOLD_STROKE)]),
        GlyphSpec("horizontal-mark", lambda c: [circle(stroke=c), line(90, 27.0, stroke=c, width=BOLD_STROKE)]),
        GlyphSpec("parallel-vertical-bars", lambda c: [circle(stroke=c), vline(-5.0, 21.0, stroke=c, width=2.9), vline(5.0, 21.0, stroke=c, width=2.9)]),
        GlyphSpec("diagonal-slash", lambda c: [circle(stroke=c), line(45, 27.0, stroke=c, width=BOLD_STROKE)]),
        GlyphSpec("parallel-horizontal-bars", lambda c: [circle(stroke=c), hline(-5.2, 21.5, stroke=c, width=2.85), hline(5.2, 21.5, stroke=c, width=2.85)]),
        GlyphSpec("large-center-dot", lambda c: [circle(stroke=c), center_dot(fill=c, radius=4.7, opacity=0.92)]),
        GlyphSpec("target-dot", lambda c: [circle(stroke=c), circle(r=7.8, stroke=c, width=3.1, opacity=0.88), center_dot(fill=c, radius=3.35, opacity=0.82)]),
        GlyphSpec("vertical-pair-dots", lambda c: [circle(stroke=c), *orbit_dots([0, 180], radius=12.9, dot_radius=3.1, fill=c, opacity=0.92)]),
        GlyphSpec("horizontal-pair-dots", lambda c: [circle(stroke=c), *orbit_dots([90, 270], radius=12.9, dot_radius=3.1, fill=c, opacity=0.92)]),
        GlyphSpec("four-inner-dots", lambda c: [circle(stroke=c), *orbit_dots(cardinal, radius=12.8, dot_radius=2.55, fill=c, opacity=0.9)]),
        GlyphSpec("cardinal-dot-core", lambda c: [circle(stroke=c), *orbit_dots(cardinal, radius=11.0, dot_radius=2.0, fill=c, opacity=0.92), center_dot(fill=c, radius=2.15, opacity=0.86)]),
        GlyphSpec("vertical-dot-core", lambda c: [circle(stroke=c), *orbit_dots([0, 180], radius=12.2, dot_radius=2.75, fill=c, opacity=0.92), center_dot(fill=c, radius=1.95, opacity=0.82)]),
        GlyphSpec("horizontal-dot-core", lambda c: [circle(stroke=c), *orbit_dots([90, 270], radius=12.2, dot_radius=2.75, fill=c, opacity=0.92), center_dot(fill=c, radius=1.95, opacity=0.82)]),
        GlyphSpec("diagonal-dot-core", lambda c: [circle(stroke=c), *orbit_dots(diagonal, radius=11.2, dot_radius=1.85, fill=c, opacity=0.90), center_dot(fill=c, radius=2.15, opacity=0.86)]),
        GlyphSpec("filled-vertical-crescents", lambda c: [circle(stroke=c), arc(312, 48, stroke=c, width=3.45, r=9.2), arc(132, 228, stroke=c, width=3.45, r=9.2), center_dot(fill=c, radius=1.95, opacity=0.84)]),
        GlyphSpec("filled-horizontal-crescents", lambda c: [circle(stroke=c), arc(42, 138, stroke=c, width=3.45, r=9.2), arc(222, 318, stroke=c, width=3.45, r=9.2), center_dot(fill=c, radius=1.95, opacity=0.84)]),
        GlyphSpec("two-vertical-bars-core", lambda c: [circle(stroke=c), vline(-5.0, 20.8, stroke=c, width=3.55), vline(5.0, 20.8, stroke=c, width=3.55), center_dot(fill=c, radius=1.55, opacity=0.74)]),
        GlyphSpec("three-horizontal-bars", lambda c: [circle(stroke=c), hline(-6.5, 22.5, stroke=c, width=3.15), hline(0, 22.5, stroke=c, width=3.15), hline(6.5, 22.5, stroke=c, width=3.15)]),
        GlyphSpec("octant-dot-core", lambda c: [circle(stroke=c), *orbit_dots(octants, radius=10.8, dot_radius=1.62, fill=c, opacity=0.90), center_dot(fill=c, radius=1.85, opacity=0.82)]),
        GlyphSpec("inner-pulse-core", lambda c: [circle(stroke=c), circle(r=8.8, stroke=c, width=2.45, opacity=0.74), center_dot(fill=c, radius=2.55, opacity=0.88)]),
        GlyphSpec("inner-diamond", lambda c: [circle(stroke=c), diamond(stroke=c, size=15.5, width=3.35)]),
        GlyphSpec("halo-four-dots", lambda c: [circle(stroke=c), circle(r=10.4, stroke=c, width=2.95, opacity=0.82), *orbit_dots(cardinal, radius=9.4, dot_radius=2.25, fill=c, opacity=0.88)]),
        GlyphSpec("three-vertical-bars", lambda c: [circle(stroke=c), vline(-7.0, 20.0, stroke=c, width=3.0), vline(0, 20.0, stroke=c, width=3.0), vline(7.0, 20.0, stroke=c, width=3.0)]),
    ]


def svg_document(elements: Iterable[str], name: str) -> str:
    # Transparent individual SVG: no rect, no preview/card background.
    body = "\n    ".join(elements)
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 0 {VIEWBOX} {VIEWBOX}" role="img" aria-label="{name}">
  <g id="glyph-{name}" vector-effect="non-scaling-stroke">
    {body}
  </g>
</svg>
"""


def contact_sheet(items: list[tuple[int, GlyphSpec, str]], selected: bool) -> str:
    cell = 128
    gap = 16
    label_h = 30
    cols = 4
    rows = math.ceil(len(items) / cols)
    width = cols * cell + (cols + 1) * gap
    height = rows * (cell + label_h) + (rows + 1) * gap
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
        f'<rect width="100%" height="100%" fill="{PREVIEW_BG}"/>',
    ]
    for position, (index, spec, filename) in enumerate(items):
        row, col = divmod(position, cols)
        x = gap + col * (cell + gap)
        y = gap + row * (cell + label_h + gap)
        parts.append(f'<rect x="{x}" y="{y}" width="{cell}" height="{cell}" rx="18" fill="{PREVIEW_CARD}" stroke="{GOLD if selected else PREVIEW_CARD_STROKE}" stroke-opacity="{0.5 if selected else 0.95}"/>')
        parts.append(f'<image href="{filename}" x="{x}" y="{y}" width="{cell}" height="{cell}"/>')
        parts.append(
            f'<text x="{x + cell / 2}" y="{y + cell + 18}" fill="#f7f1df" '
            f'font-family="-apple-system, BlinkMacSystemFont, SF Pro Text, sans-serif" '
            f'font-size="9.5" text-anchor="middle">{index:02d} · {spec.name}</text>'
        )
    parts.append("</svg>\n")
    return "\n".join(parts)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", default="tools/generated_vector_circle_glyphs_v2", help="Output directory")
    parser.add_argument("--count", type=int, default=24, help="Number of glyphs to export")
    parser.add_argument("--selected", action="store_true", help="Render selected/gold state")
    args = parser.parse_args()

    out_dir = Path(args.out)
    out_dir.mkdir(parents=True, exist_ok=True)
    # Keep output deterministic: remove stale glyph files from older design passes.
    for stale in out_dir.glob("vector-circle-glyph-*.svg"):
        stale.unlink()
    color = GOLD if args.selected else MUTED
    specs = glyphs()

    manifest = []
    contact_items: list[tuple[int, GlyphSpec, str]] = []
    for index in range(args.count):
        spec = specs[index % len(specs)]
        filename = f"vector-circle-glyph-{index:02d}-{spec.name}.svg"
        svg = svg_document(spec.draw(color), spec.name)
        (out_dir / filename).write_text(svg, encoding="utf-8")
        manifest.append({
            "index": index,
            "name": spec.name,
            "file": filename,
            "viewBox": f"0 0 {VIEWBOX} {VIEWBOX}",
            "transparentBackground": True,
            "silhouetteFirst": True,
            "center": [CENTER, CENTER],
            "targetRaster": "24pt @2x = 48px; project-sized outer ring; no detail below ~2.5px",
            "radius": RADIUS,
            "stroke": STROKE,
            "color": color,
            "selected": args.selected,
        })
        contact_items.append((index, spec, filename))

    (out_dir / "manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    (out_dir / "contact-sheet.svg").write_text(contact_sheet(contact_items, args.selected), encoding="utf-8")
    print(f"Generated {args.count} high-legibility transparent SVG glyphs in {out_dir}")
    print(f"Contact sheet: {out_dir / 'contact-sheet.svg'}")


if __name__ == "__main__":
    main()
