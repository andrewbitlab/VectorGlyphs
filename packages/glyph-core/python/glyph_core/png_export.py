from __future__ import annotations

import math
import re
import tempfile
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Iterable

try:
    from PIL import Image, ImageDraw
except ModuleNotFoundError:  # pragma: no cover - exercised only in unprepared environments
    Image = None
    ImageDraw = None

HEX_RE = re.compile(r"^#?([0-9a-fA-F]{6})([0-9a-fA-F]{2})?$")
NUMBER_RE = re.compile(r"-?\d+(?:\.\d+)?")


def _strip_ns(tag: str) -> str:
    return tag.rsplit("}", 1)[-1]


def _color(value: str | None, current: str, opacity: float = 1.0) -> tuple[int, int, int, int] | None:
    if value is None or value == "none":
        return None
    if value == "currentColor":
        value = current
    match = HEX_RE.match(value)
    if not match:
        return None
    rgb = match.group(1)
    alpha_hex = match.group(2)
    alpha = int(alpha_hex, 16) if alpha_hex else 255
    alpha = max(0, min(255, round(alpha * opacity)))
    return (int(rgb[0:2], 16), int(rgb[2:4], 16), int(rgb[4:6], 16), alpha)


def _float(attrs: dict[str, str], name: str, default: float = 0.0) -> float:
    try:
        return float(attrs.get(name, default))
    except ValueError:
        return default


def _view_box(root: ET.Element) -> tuple[float, float, float, float]:
    raw = root.attrib.get("viewBox", "0 0 48 48")
    parts = [float(part) for part in raw.replace(",", " ").split()]
    if len(parts) != 4:
        return (0.0, 0.0, 48.0, 48.0)
    return tuple(parts)  # type: ignore[return-value]


def _scale_point(x: float, y: float, min_x: float, min_y: float, scale: float) -> tuple[float, float]:
    return ((x - min_x) * scale, (y - min_y) * scale)


def _draw_circle(draw, attrs: dict[str, str], current: str, view: tuple[float, float, float, float], scale: float) -> None:
    min_x, min_y, _, _ = view
    cx = _float(attrs, "cx")
    cy = _float(attrs, "cy")
    r = _float(attrs, "r")
    opacity = _float(attrs, "opacity", 1.0)
    x0, y0 = _scale_point(cx - r, cy - r, min_x, min_y, scale)
    x1, y1 = _scale_point(cx + r, cy + r, min_x, min_y, scale)
    fill = _color(attrs.get("fill"), current, opacity)
    stroke = _color(attrs.get("stroke"), current, opacity)
    width = max(1, round(_float(attrs, "stroke-width", 1.0) * scale))
    if fill:
        draw.ellipse([x0, y0, x1, y1], fill=fill)
    if stroke:
        draw.ellipse([x0, y0, x1, y1], outline=stroke, width=width)


def _draw_line(draw, attrs: dict[str, str], current: str, view: tuple[float, float, float, float], scale: float) -> None:
    min_x, min_y, _, _ = view
    opacity = _float(attrs, "opacity", 1.0)
    stroke = _color(attrs.get("stroke", "currentColor"), current, opacity)
    if stroke is None:
        return
    p1 = _scale_point(_float(attrs, "x1"), _float(attrs, "y1"), min_x, min_y, scale)
    p2 = _scale_point(_float(attrs, "x2"), _float(attrs, "y2"), min_x, min_y, scale)
    width = max(1, round(_float(attrs, "stroke-width", 1.0) * scale))
    draw.line([p1, p2], fill=stroke, width=width)


def _polar(cx: float, cy: float, r: float, angle_deg: float) -> tuple[float, float]:
    angle = math.radians(angle_deg - 90)
    return cx + r * math.cos(angle), cy + r * math.sin(angle)


def _angle_from_point(cx: float, cy: float, x: float, y: float) -> float:
    return (math.degrees(math.atan2(y - cy, x - cx)) + 90) % 360


def _arc_points(start_angle: float, end_angle: float, radius: float, large_arc: int, cx: float, cy: float) -> list[tuple[float, float]]:
    span = (end_angle - start_angle) % 360
    if large_arc and span < 180:
        span += 360
    if not large_arc and span > 180:
        span -= 360
    steps = max(12, int(abs(span) / 6))
    return [_polar(cx, cy, radius, start_angle + span * i / steps) for i in range(steps + 1)]


def _draw_path(draw, attrs: dict[str, str], current: str, view: tuple[float, float, float, float], scale: float) -> None:
    d = attrs.get("d", "")
    nums = [float(n) for n in NUMBER_RE.findall(d)]
    if not nums:
        return
    min_x, min_y, width_vb, height_vb = view
    opacity = _float(attrs, "opacity", 1.0)
    stroke = _color(attrs.get("stroke", "currentColor"), current, opacity)
    width = max(1, round(_float(attrs, "stroke-width", 1.0) * scale))
    if " A " in f" {d} " and len(nums) >= 9 and stroke is not None:
        sx, sy, rx, _ry, _rot, large_arc, _sweep, ex, ey = nums[:9]
        cx = min_x + width_vb / 2
        cy = min_y + height_vb / 2
        start = _angle_from_point(cx, cy, sx, sy)
        end = _angle_from_point(cx, cy, ex, ey)
        points = [_scale_point(x, y, min_x, min_y, scale) for x, y in _arc_points(start, end, rx, int(large_arc), cx, cy)]
        draw.line(points, fill=stroke, width=width)
        return
    if " L " in f" {d} " and len(nums) >= 4:
        points = list(zip(nums[0::2], nums[1::2]))
        scaled = [_scale_point(x, y, min_x, min_y, scale) for x, y in points]
        fill = _color(attrs.get("fill"), current, opacity)
        if fill and d.strip().endswith("Z"):
            draw.polygon(scaled, fill=fill)
        if stroke:
            if d.strip().endswith("Z") and scaled:
                scaled = [*scaled, scaled[0]]
            draw.line(scaled, fill=stroke, width=width)


def _draw_rect(draw, attrs: dict[str, str], current: str, view: tuple[float, float, float, float], scale: float) -> None:
    min_x, min_y, _, _ = view
    x = _float(attrs, "x", 0.0)
    y = _float(attrs, "y", 0.0)
    w = _float(attrs, "width", 48.0)
    h = _float(attrs, "height", 48.0)
    fill = _color(attrs.get("fill"), current, _float(attrs, "opacity", 1.0))
    if fill:
        p0 = _scale_point(x, y, min_x, min_y, scale)
        p1 = _scale_point(x + w, y + h, min_x, min_y, scale)
        draw.rectangle([p0, p1], fill=fill)


def export_png(svg: str, size: int, background: str | None = None) -> bytes:
    if size not in {512, 1024, 2048, 4096}:
        raise ValueError("size must be one of 512, 1024, 2048, 4096")
    if Image is None or ImageDraw is None:
        raise RuntimeError("Pillow is required for PNG export")

    root = ET.fromstring(svg)
    view = _view_box(root)
    _, _, width_vb, height_vb = view
    scale = size / max(width_vb, height_vb)
    current = root.attrib.get("color", "#111827")
    bg = _color(background, current) if background else None
    image = Image.new("RGBA", (size, size), bg or (0, 0, 0, 0))
    draw = ImageDraw.Draw(image)

    for element in root.iter():
        tag = _strip_ns(element.tag)
        attrs = dict(element.attrib)
        if tag == "rect" and background is None:
            _draw_rect(draw, attrs, current, view, scale)
        elif tag == "circle":
            _draw_circle(draw, attrs, current, view, scale)
        elif tag == "line":
            _draw_line(draw, attrs, current, view, scale)
        elif tag == "path":
            _draw_path(draw, attrs, current, view, scale)

    with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as handle:
        temp_path = Path(handle.name)
    try:
        image.save(temp_path, format="PNG")
        return temp_path.read_bytes()
    finally:
        temp_path.unlink(missing_ok=True)
