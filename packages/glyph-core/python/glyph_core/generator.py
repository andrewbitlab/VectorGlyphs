from __future__ import annotations

import math
import random
from dataclasses import dataclass
from typing import Callable, Iterable

from .specs import Glyph, GlyphGenerationSpec, GlyphSet

VIEWBOX = 48
CENTER = 24.0
RADIUS = 17.6
BASE_STROKE = 3.6
INNER_STROKE = 2.65
BOLD_STROKE = 4.35


def fmt(value: float) -> str:
    text = f"{value:.4f}".rstrip("0").rstrip(".")
    return text if text != "-0" else "0"


def polar(cx: float, cy: float, r: float, angle_deg: float) -> tuple[float, float]:
    # 0° at 12 o'clock, clockwise-positive, matching the original source generator.
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


def circle(r: float = RADIUS, width: float = BASE_STROKE, opacity: float = 1.0) -> str:
    return (
        f'<circle cx="{fmt(CENTER)}" cy="{fmt(CENTER)}" r="{fmt(r)}" '
        f'fill="none" stroke="currentColor" stroke-width="{fmt(width)}" '
        f'stroke-linecap="round" stroke-linejoin="round"{opacity_attr(opacity)}/>'
    )


def arc(start: float, end: float, width: float = BASE_STROKE, r: float = RADIUS, opacity: float = 1.0) -> str:
    return (
        f'<path d="{arc_path(start, end, r)}" fill="none" stroke="currentColor" '
        f'stroke-width="{fmt(width)}" stroke-linecap="round" stroke-linejoin="round"{opacity_attr(opacity)}/>'
    )


def line(angle: float, length: float, width: float = BOLD_STROKE, opacity: float = 1.0) -> str:
    x1, y1 = polar(CENTER, CENTER, length / 2, angle)
    x2, y2 = polar(CENTER, CENTER, length / 2, angle + 180)
    return (
        f'<line x1="{fmt(x1)}" y1="{fmt(y1)}" x2="{fmt(x2)}" y2="{fmt(y2)}" '
        f'stroke="currentColor" stroke-width="{fmt(width)}" stroke-linecap="round"{opacity_attr(opacity)}/>'
    )


def hline(y_offset: float, length: float, width: float = INNER_STROKE, opacity: float = 1.0) -> str:
    y = CENTER + y_offset
    return (
        f'<line x1="{fmt(CENTER - length / 2)}" y1="{fmt(y)}" x2="{fmt(CENTER + length / 2)}" y2="{fmt(y)}" '
        f'stroke="currentColor" stroke-width="{fmt(width)}" stroke-linecap="round"{opacity_attr(opacity)}/>'
    )


def vline(x_offset: float, length: float, width: float = INNER_STROKE, opacity: float = 1.0) -> str:
    x = CENTER + x_offset
    return (
        f'<line x1="{fmt(x)}" y1="{fmt(CENTER - length / 2)}" x2="{fmt(x)}" y2="{fmt(CENTER + length / 2)}" '
        f'stroke="currentColor" stroke-width="{fmt(width)}" stroke-linecap="round"{opacity_attr(opacity)}/>'
    )


def dot(angle: float, radius_from_center: float = RADIUS, dot_radius: float = 2.0, opacity: float = 1.0) -> str:
    x, y = polar(CENTER, CENTER, radius_from_center, angle)
    return f'<circle cx="{fmt(x)}" cy="{fmt(y)}" r="{fmt(dot_radius)}" fill="currentColor"{opacity_attr(opacity)}/>'


def center_dot(radius: float = 3.0, opacity: float = 1.0) -> str:
    return f'<circle cx="{fmt(CENTER)}" cy="{fmt(CENTER)}" r="{fmt(radius)}" fill="currentColor"{opacity_attr(opacity)}/>'


def diamond(size: float = 15.0, width: float = INNER_STROKE, opacity: float = 1.0) -> str:
    half = size / 2
    points = [(CENTER, CENTER - half), (CENTER + half, CENTER), (CENTER, CENTER + half), (CENTER - half, CENTER)]
    d = "M " + " L ".join(f"{fmt(x)} {fmt(y)}" for x, y in points) + " Z"
    return (
        f'<path d="{d}" fill="none" stroke="currentColor" stroke-width="{fmt(width)}" '
        f'stroke-linecap="round" stroke-linejoin="round"{opacity_attr(opacity)}/>'
    )


def orbit_dots(angles: Iterable[float], radius: float = RADIUS, dot_radius: float = 1.85, opacity: float = 1.0) -> list[str]:
    return [dot(angle, radius_from_center=radius, dot_radius=dot_radius, opacity=opacity) for angle in angles]


@dataclass(frozen=True)
class GlyphTemplate:
    name: str
    draw: Callable[[], list[str]]
    tags: tuple[str, ...]


def base_templates() -> list[GlyphTemplate]:
    cardinal = [0, 90, 180, 270]
    diagonal = [45, 135, 225, 315]
    octants = [0, 45, 90, 135, 180, 225, 270, 315]
    return [
        GlyphTemplate("silence-ring", lambda: [circle()], ("minimal", "simple")),
        GlyphTemplate("vertical-mark", lambda: [circle(), line(0, 27.0)], ("minimal", "simple")),
        GlyphTemplate("horizontal-mark", lambda: [circle(), line(90, 27.0)], ("minimal", "simple")),
        GlyphTemplate("parallel-vertical-bars", lambda: [circle(), vline(-5.0, 21.0, width=2.9), vline(5.0, 21.0, width=2.9)], ("dashboard", "balanced")),
        GlyphTemplate("diagonal-slash", lambda: [circle(), line(45, 27.0)], ("tech", "simple")),
        GlyphTemplate("parallel-horizontal-bars", lambda: [circle(), hline(-5.2, 21.5, width=2.85), hline(5.2, 21.5, width=2.85)], ("dashboard", "balanced")),
        GlyphTemplate("large-center-dot", lambda: [circle(), center_dot(radius=4.7, opacity=0.92)], ("premium-ui", "simple")),
        GlyphTemplate("target-dot", lambda: [circle(), circle(r=7.8, width=3.1, opacity=0.88), center_dot(radius=3.35, opacity=0.82)], ("tech", "balanced")),
        GlyphTemplate("vertical-pair-dots", lambda: [circle(), *orbit_dots([0, 180], radius=12.9, dot_radius=3.1, opacity=0.92)], ("organic", "balanced")),
        GlyphTemplate("horizontal-pair-dots", lambda: [circle(), *orbit_dots([90, 270], radius=12.9, dot_radius=3.1, opacity=0.92)], ("organic", "balanced")),
        GlyphTemplate("four-inner-dots", lambda: [circle(), *orbit_dots(cardinal, radius=12.8, dot_radius=2.55, opacity=0.9)], ("premium-ui", "dense")),
        GlyphTemplate("cardinal-dot-core", lambda: [circle(), *orbit_dots(cardinal, radius=11.0, dot_radius=2.0, opacity=0.92), center_dot(radius=2.15, opacity=0.86)], ("mystic", "dense")),
        GlyphTemplate("vertical-dot-core", lambda: [circle(), *orbit_dots([0, 180], radius=12.2, dot_radius=2.75, opacity=0.92), center_dot(radius=1.95, opacity=0.82)], ("premium-ui", "balanced")),
        GlyphTemplate("horizontal-dot-core", lambda: [circle(), *orbit_dots([90, 270], radius=12.2, dot_radius=2.75, opacity=0.92), center_dot(radius=1.95, opacity=0.82)], ("premium-ui", "balanced")),
        GlyphTemplate("diagonal-dot-core", lambda: [circle(), *orbit_dots(diagonal, radius=11.2, dot_radius=1.85, opacity=0.90), center_dot(radius=2.15, opacity=0.86)], ("mystic", "dense")),
        GlyphTemplate("filled-vertical-crescents", lambda: [circle(), arc(312, 48, width=3.45, r=9.2), arc(132, 228, width=3.45, r=9.2), center_dot(radius=1.95, opacity=0.84)], ("organic", "balanced")),
        GlyphTemplate("filled-horizontal-crescents", lambda: [circle(), arc(42, 138, width=3.45, r=9.2), arc(222, 318, width=3.45, r=9.2), center_dot(radius=1.95, opacity=0.84)], ("organic", "balanced")),
        GlyphTemplate("two-vertical-bars-core", lambda: [circle(), vline(-5.0, 20.8, width=3.55), vline(5.0, 20.8, width=3.55), center_dot(radius=1.55, opacity=0.74)], ("dashboard", "balanced")),
        GlyphTemplate("three-horizontal-bars", lambda: [circle(), hline(-6.5, 22.5, width=3.15), hline(0, 22.5, width=3.15), hline(6.5, 22.5, width=3.15)], ("dashboard", "dense")),
        GlyphTemplate("octant-dot-core", lambda: [circle(), *orbit_dots(octants, radius=10.8, dot_radius=1.62, opacity=0.90), center_dot(radius=1.85, opacity=0.82)], ("mystic", "dense")),
        GlyphTemplate("inner-pulse-core", lambda: [circle(), circle(r=8.8, width=2.45, opacity=0.74), center_dot(radius=2.55, opacity=0.88)], ("premium-ui", "balanced")),
        GlyphTemplate("inner-diamond", lambda: [circle(), diamond(size=15.5, width=3.35)], ("geometric", "simple")),
        GlyphTemplate("halo-four-dots", lambda: [circle(), circle(r=10.4, width=2.95, opacity=0.82), *orbit_dots(cardinal, radius=9.4, dot_radius=2.25, opacity=0.88)], ("geometric", "dense")),
        GlyphTemplate("three-vertical-bars", lambda: [circle(), vline(-7.0, 20.0, width=3.0), vline(0, 20.0, width=3.0), vline(7.0, 20.0, width=3.0)], ("dashboard", "dense")),
    ]


def complexity_rank(template: GlyphTemplate) -> int:
    if "simple" in template.tags:
        return 1
    if "dense" in template.tags:
        return 3
    return 2


def ordered_templates(spec: GlyphGenerationSpec) -> list[GlyphTemplate]:
    templates = base_templates()
    if spec.complexity == "simple":
        preferred = [t for t in templates if complexity_rank(t) <= 2]
    elif spec.complexity == "dense":
        preferred = [t for t in templates if complexity_rank(t) >= 2]
    else:
        preferred = templates[:]

    if spec.motif_families:
        motif_set = set(spec.motif_families)
        motif_matches = [t for t in preferred if motif_set.intersection(t.tags)]
        if motif_matches:
            preferred = motif_matches

    style_matches = [t for t in preferred if spec.style in t.tags]
    remaining = [t for t in preferred if t not in style_matches]
    rng = random.Random(f"{spec.seed}|{spec.style}|{spec.complexity}|{','.join(spec.motif_families)}")
    rng.shuffle(style_matches)
    rng.shuffle(remaining)
    ordered = style_matches + remaining
    if not ordered:
        ordered = templates[:]
        rng.shuffle(ordered)
    return ordered


def generate_glyph_set(spec: GlyphGenerationSpec) -> GlyphSet:
    templates = ordered_templates(spec)
    glyphs: list[Glyph] = []
    for index in range(spec.count):
        template = templates[index % len(templates)]
        cycle = index // len(templates)
        name = template.name if cycle == 0 else f"{template.name}-{cycle + 1}"
        glyphs.append(
            Glyph(
                id=f"glyph_{index + 1:03d}",
                name=name,
                elements=tuple(template.draw()),
                template=template.name,
                tags=template.tags,
            )
        )
    return GlyphSet(spec_hash=spec.hash(), glyphs=tuple(glyphs))
