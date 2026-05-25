from __future__ import annotations

from dataclasses import asdict, dataclass
import io
import math
import os
import re
import shutil
import subprocess
import tempfile
from pathlib import Path
from typing import Iterable

import numpy as np
from PIL import Image, ImageChops
from scipy import ndimage as ndi
from skimage import measure, morphology
from skimage.filters import threshold_otsu, threshold_local
from skimage.metrics import structural_similarity


@dataclass(frozen=True)
class BoundingBox:
    left: int
    top: int
    right: int
    bottom: int

    @property
    def width(self) -> int:
        return self.right - self.left

    @property
    def height(self) -> int:
        return self.bottom - self.top

    def expanded(self, pad: int, width: int, height: int) -> "BoundingBox":
        return BoundingBox(
            max(0, self.left - pad),
            max(0, self.top - pad),
            min(width, self.right + pad),
            min(height, self.bottom + pad),
        )

    def to_dict(self) -> dict[str, int]:
        return asdict(self)


@dataclass(frozen=True)
class GlyphCrop:
    index: int
    bbox: BoundingBox
    image: Image.Image
    mask: np.ndarray
    foreground_pixels: int


@dataclass(frozen=True)
class VectorizationResult:
    svg: str
    backend: str
    score: SimilarityScore
    accepted: bool

    def to_dict(self) -> dict[str, object]:
        return {
            "backend": self.backend,
            "accepted": self.accepted,
            "score": self.score.to_dict(),
        }


@dataclass(frozen=True)
class SegmenterConfig:
    min_area_ratio: float = 0.00008
    max_glyphs: int = 250
    min_component_size_px: int = 12
    padding_ratio: float = 0.16
    merge_radius_ratio: float = 0.012


@dataclass(frozen=True)
class VectorizerConfig:
    stroke_color: str = "#000000"
    simplify_tolerance: float = 0.45
    precision: int = 2
    trace_mode: str = "lossless-runs"


@dataclass(frozen=True)
class SimilarityScore:
    ssim: float
    foreground_iou: float
    mean_abs_error: float
    pixel_error_ratio: float

    def to_dict(self) -> dict[str, float]:
        return asdict(self)


def _as_grayscale_array(image: Image.Image) -> np.ndarray:
    return np.asarray(image.convert("L"), dtype=np.float32) / 255.0


def _odd_block_size(size: int) -> int:
    block = max(15, int(size * 0.045))
    return block + 1 if block % 2 == 0 else block


def create_monochrome_mask(image: Image.Image, *, adaptive: bool = True) -> np.ndarray:
    """Return True for foreground ink, regardless of light/dark source background.

    The first vectorizer.app iteration is intentionally monochrome. This function
    converts arbitrary black-on-white, white-on-black, or slightly tinted source
    sheets into a clean boolean ink mask while preserving thin icon strokes.
    """
    gray = _as_grayscale_array(image)
    height, width = gray.shape
    border_width = max(2, min(height, width) // 30)
    border = np.concatenate(
        [
            gray[:border_width, :].ravel(),
            gray[-border_width:, :].ravel(),
            gray[:, :border_width].ravel(),
            gray[:, -border_width:].ravel(),
        ]
    )
    background_level = float(np.median(border))

    try:
        otsu = float(threshold_otsu(gray))
    except ValueError:
        otsu = 0.5

    # Global polarity is anchored to the border, because user uploads are usually
    # sheets/screenshots with mostly background around the edge. Otsu alone can
    # return an extreme threshold for synthetic black/white art, so we blend the
    # border level with a foreground percentile.
    if background_level >= 0.5:
        dark_percentile = float(np.percentile(gray, 3))
        threshold = float(np.clip((background_level + min(otsu, dark_percentile + 0.08)) / 2, 0.08, 0.94))
        mask = gray < threshold
        if adaptive and min(height, width) >= 96:
            block = _odd_block_size(min(height, width))
            local = threshold_local(gray, block_size=block, offset=0)
            mask |= gray < np.minimum(local - 0.035, threshold)
    else:
        light_percentile = float(np.percentile(gray, 97))
        threshold = float(np.clip((background_level + max(otsu, light_percentile - 0.08)) / 2, 0.06, 0.92))
        mask = gray > threshold
        if adaptive and min(height, width) >= 96:
            block = _odd_block_size(min(height, width))
            local = threshold_local(gray, block_size=block, offset=0)
            mask |= gray > np.maximum(local + 0.035, threshold)

    min_object = max(4, int(height * width * 0.000002))
    mask = morphology.remove_small_objects(mask.astype(bool), max_size=max(1, min_object - 1))
    mask = morphology.remove_small_holes(mask, max_size=max(1, int(height * width * 0.000001) - 1))
    return np.asarray(mask, dtype=bool)


def _component_boxes(label_image: np.ndarray, source_mask: np.ndarray, min_area: int) -> list[tuple[BoundingBox, int]]:
    boxes: list[tuple[BoundingBox, int]] = []
    for region in measure.regionprops(label_image):
        top, left, bottom, right = region.bbox
        source_area = int(source_mask[top:bottom, left:right].sum())
        if source_area < min_area:
            continue
        if right - left < 4 or bottom - top < 4:
            continue
        boxes.append((BoundingBox(left, top, right, bottom), source_area))
    return boxes


def _choose_grouping(mask: np.ndarray, config: SegmenterConfig) -> list[tuple[BoundingBox, int]]:
    height, width = mask.shape
    min_area = max(config.min_component_size_px, int(height * width * config.min_area_ratio))
    base_radius = max(1, int(min(height, width) * config.merge_radius_ratio))
    radii = sorted(set([0, base_radius, base_radius * 2, base_radius * 3, base_radius * 5]))
    best: list[tuple[BoundingBox, int]] = []
    best_score = -10**9

    for radius in radii:
        # Rectangular max-filter dilation is intentionally used here instead of
        # skimage's disk dilation: for multi-megapixel uploaded sheets it is two
        # orders of magnitude faster, and grouping is only a coarse step before
        # every box is tightened back to the original ink mask.
        grouped = mask if radius == 0 else ndi.maximum_filter(mask, size=(radius * 2 + 1, radius * 2 + 1))
        labels = measure.label(grouped, connectivity=2)
        boxes = _component_boxes(labels, mask, min_area)
        if not boxes:
            continue
        median_area = float(np.median([area for _, area in boxes])) if boxes else 0
        balanced = sum(1 for box, area in boxes if median_area * 0.12 <= area <= median_area * 9 and 0.12 <= box.width / max(1, box.height) <= 8.0)
        median_box_area = float(np.median([box.width * box.height for box, _ in boxes]))
        tiny_boxes = sum(1 for box, _ in boxes if box.width < min(width, height) * 0.045 or box.height < min(width, height) * 0.045)
        score = balanced * 24 + math.log1p(median_box_area) * 9 + radius * 2.5 - tiny_boxes * 12 - len(boxes) * 0.65
        if score > best_score:
            best = boxes
            best_score = score

    if not best:
        labels = measure.label(mask, connectivity=2)
        best = _component_boxes(labels, mask, min_area)
    return best


def _tighten_bbox(mask: np.ndarray, bbox: BoundingBox) -> BoundingBox | None:
    crop = mask[bbox.top:bbox.bottom, bbox.left:bbox.right]
    ys, xs = np.where(crop)
    if len(xs) == 0:
        return None
    return BoundingBox(
        bbox.left + int(xs.min()),
        bbox.top + int(ys.min()),
        bbox.left + int(xs.max()) + 1,
        bbox.top + int(ys.max()) + 1,
    )


def _sort_boxes_reading_order(items: list[tuple[BoundingBox, int]]) -> list[tuple[BoundingBox, int]]:
    if not items:
        return []
    median_h = float(np.median([box.height for box, _ in items]))
    tolerance = max(8.0, median_h * 0.65)
    sorted_items = sorted(items, key=lambda item: ((item[0].top + item[0].bottom) / 2, item[0].left))
    rows: list[list[tuple[BoundingBox, int]]] = []
    for item in sorted_items:
        cy = (item[0].top + item[0].bottom) / 2
        for row in rows:
            row_cy = np.mean([(box.top + box.bottom) / 2 for box, _ in row])
            if abs(cy - row_cy) <= tolerance:
                row.append(item)
                break
        else:
            rows.append([item])
    ordered: list[tuple[BoundingBox, int]] = []
    for row in rows:
        ordered.extend(sorted(row, key=lambda item: item[0].left))
    return ordered


def segment_glyph_sheet(image: Image.Image, mask: np.ndarray, config: SegmenterConfig | None = None) -> list[GlyphCrop]:
    config = config or SegmenterConfig()
    if mask.ndim != 2:
        raise ValueError("mask must be a 2D boolean array")
    height, width = mask.shape
    candidates: list[tuple[BoundingBox, int]] = []
    for bbox, area in _choose_grouping(mask, config):
        tight = _tighten_bbox(mask, bbox)
        if tight is None:
            continue
        pad = max(3, int(max(tight.width, tight.height) * config.padding_ratio))
        expanded = tight.expanded(pad, width, height)
        # Drop obvious title/watermark rules: very wide, very thin, or huge regions.
        if expanded.width / max(1, expanded.height) > 9 or expanded.height / max(1, expanded.width) > 9:
            continue
        if expanded.width * expanded.height > width * height * 0.35:
            continue
        candidates.append((expanded, area))

    ordered = _sort_boxes_reading_order(candidates)[: config.max_glyphs]
    glyphs: list[GlyphCrop] = []
    for index, (bbox, area) in enumerate(ordered, start=1):
        crop_image = image.crop((bbox.left, bbox.top, bbox.right, bbox.bottom)).convert("RGBA")
        crop_mask = mask[bbox.top:bbox.bottom, bbox.left:bbox.right].copy()
        glyphs.append(GlyphCrop(index=index, bbox=bbox, image=crop_image, mask=crop_mask, foreground_pixels=area))
    return glyphs


def _fmt(value: float, precision: int) -> str:
    text = f"{float(value):.{precision}f}".rstrip("0").rstrip(".")
    return "0" if text == "-0" else text


def _contour_to_path(contour: np.ndarray, precision: int) -> str:
    if len(contour) < 3:
        return ""
    # skimage returns row, col; SVG expects x, y.
    commands = [f"M {_fmt(contour[0, 1], precision)} {_fmt(contour[0, 0], precision)}"]
    commands.extend(f"L {_fmt(point[1], precision)} {_fmt(point[0], precision)}" for point in contour[1:])
    commands.append("Z")
    return " ".join(commands)


def _safe_hex(color: str) -> str:
    if not re.fullmatch(r"#[0-9a-fA-F]{6}([0-9a-fA-F]{2})?", color):
        raise ValueError("stroke_color must be a hex color")
    return color


def _runs_to_path(mask: np.ndarray) -> str:
    commands: list[str] = []
    height, width = mask.shape
    for y in range(height):
        x = 0
        while x < width:
            if not mask[y, x]:
                x += 1
                continue
            start = x
            while x < width and mask[y, x]:
                x += 1
            end = x
            commands.append(f"M {start} {y} L {end} {y} L {end} {y + 1} L {start} {y + 1} Z")
    return " ".join(commands)


def vectorize_mask_to_svg(mask: np.ndarray, config: VectorizerConfig | None = None) -> str:
    config = config or VectorizerConfig()
    if mask.ndim != 2:
        raise ValueError("mask must be a 2D boolean array")
    height, width = mask.shape
    if config.trace_mode == "lossless-runs":
        path_data = _runs_to_path(mask.astype(bool))
    elif config.trace_mode == "contour":
        padded = np.pad(mask.astype(float), 1, mode="constant", constant_values=0)
        contours = measure.find_contours(padded, 0.5, fully_connected="high", positive_orientation="high")
        paths: list[str] = []
        for contour in contours:
            contour = contour - 1
            if config.simplify_tolerance > 0:
                contour = measure.approximate_polygon(contour, tolerance=config.simplify_tolerance)
            path = _contour_to_path(contour, config.precision)
            if path:
                paths.append(path)
        path_data = " ".join(paths)
    else:
        raise ValueError("trace_mode must be 'lossless-runs' or 'contour'")

    color = _safe_hex(config.stroke_color)
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" '
        f'viewBox="0 0 {width} {height}" role="img" data-trace-mode="{config.trace_mode}">\n'
        f'  <path d="{path_data}" fill="{color}" fill-rule="evenodd" clip-rule="evenodd"/>\n'
        "</svg>\n"
    )


def _write_mask_as_pbm(mask: np.ndarray, path: Path) -> None:
    image = Image.fromarray(np.where(mask, 0, 255).astype(np.uint8), "L").convert("1")
    image.save(path)


def _sanitize_external_svg(svg: str, backend: str) -> str:
    svg = re.sub(r"<\?xml[^>]*>\s*", "", svg, flags=re.IGNORECASE)
    svg = re.sub(r"<!DOCTYPE[\s\S]*?>\s*", "", svg, flags=re.IGNORECASE)
    svg = re.sub(r"<metadata[\s\S]*?</metadata>\s*", "", svg, flags=re.IGNORECASE)
    svg = re.sub(r"<!--.*?-->\s*", "", svg, flags=re.DOTALL)
    svg = svg.replace("http://www.w3.org/TR/2001/REC-SVG-20010904/DTD/svg10.dtd", "")
    svg = re.sub(r"<svg\b", f'<svg data-trace-mode="{backend}"', svg, count=1)
    return svg.strip() + "\n"


def _trace_mask_with_potrace(mask: np.ndarray, config: VectorizerConfig) -> str | None:
    if shutil.which("potrace") is None:
        return None
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        pbm_path = tmp_path / "glyph.pbm"
        svg_path = tmp_path / "glyph.svg"
        _write_mask_as_pbm(mask.astype(bool), pbm_path)
        command = [
            "potrace",
            "-s",
            "--flat",
            "--turdsize",
            "1",
            "--opttolerance",
            "0.2",
            "--alphamax",
            "1.0",
            "--color",
            _safe_hex(config.stroke_color),
            "-o",
            str(svg_path),
            str(pbm_path),
        ]
        subprocess.run(command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        return _sanitize_external_svg(svg_path.read_text(encoding="utf-8"), "potrace")


def _trace_mask_with_vtracer(mask: np.ndarray, config: VectorizerConfig) -> str | None:
    try:
        import vtracer  # type: ignore[import-not-found]
    except Exception:
        return None
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        input_path = tmp_path / "glyph.png"
        output_path = tmp_path / "glyph.svg"
        Image.fromarray(np.where(mask, 0, 255).astype(np.uint8), "L").convert("RGB").save(input_path)
        vtracer.convert_image_to_svg_py(
            str(input_path),
            str(output_path),
            colormode="binary",
            hierarchical="stacked",
            mode="spline",
            filter_speckle=1,
            color_precision=6,
            layer_difference=16,
            corner_threshold=60,
            length_threshold=3.5,
            max_iterations=10,
            splice_threshold=45,
            path_precision=max(1, config.precision),
        )
        return _sanitize_external_svg(output_path.read_text(encoding="utf-8"), "vtracer")


def trace_mask_to_svg_best_effort(
    mask: np.ndarray,
    config: VectorizerConfig | None = None,
    *,
    preferred_backend: str = "auto",
    min_ssim: float = 0.985,
    min_iou: float = 0.97,
) -> VectorizationResult:
    config = config or VectorizerConfig()
    reference = mask_to_reference_image(mask)
    candidates: list[tuple[str, str]] = []

    backend_order = ["potrace", "vtracer"] if preferred_backend == "auto" else [preferred_backend]
    for backend in backend_order:
        svg: str | None = None
        if backend == "potrace":
            svg = _trace_mask_with_potrace(mask, config)
        elif backend == "vtracer":
            svg = _trace_mask_with_vtracer(mask, config)
        elif backend == "contour":
            svg = vectorize_mask_to_svg(mask, VectorizerConfig(stroke_color=config.stroke_color, simplify_tolerance=config.simplify_tolerance, precision=config.precision, trace_mode="contour"))
        if svg:
            candidates.append((backend, svg))

    lossless_svg = vectorize_mask_to_svg(mask, VectorizerConfig(stroke_color=config.stroke_color, simplify_tolerance=0, precision=config.precision, trace_mode="lossless-runs"))
    candidates.append(("lossless-runs", lossless_svg))

    best: VectorizationResult | None = None
    for backend, svg in candidates:
        try:
            rendered = render_svg_to_png(svg, mask.shape[1], mask.shape[0])
            score = compare_images(reference, rendered)
        except Exception:
            continue
        accepted = score.ssim >= min_ssim and score.foreground_iou >= min_iou
        result = VectorizationResult(svg=svg, backend=backend, score=score, accepted=accepted)
        if accepted:
            return result
        if best is None or (score.ssim, score.foreground_iou) > (best.score.ssim, best.score.foreground_iou):
            best = result
    if best is not None:
        return best
    rendered = render_svg_to_png(lossless_svg, mask.shape[1], mask.shape[0])
    return VectorizationResult(svg=lossless_svg, backend="lossless-runs", score=compare_images(reference, rendered), accepted=True)


def _parse_own_path_polygons(svg: str) -> list[list[tuple[float, float]]]:
    match = re.search(r'<path[^>]*\sd="([^"]*)"', svg)
    if not match:
        return []
    tokens = re.findall(r"[MLZ]|-?\d+(?:\.\d+)?", match.group(1))
    polygons: list[list[tuple[float, float]]] = []
    current: list[tuple[float, float]] = []
    index = 0
    command = ""
    while index < len(tokens):
        token = tokens[index]
        if token in {"M", "L", "Z"}:
            command = token
            index += 1
            if command == "Z" and current:
                polygons.append(current)
                current = []
            continue
        if command in {"M", "L"} and index + 1 < len(tokens):
            x = float(tokens[index])
            y = float(tokens[index + 1])
            current.append((x, y))
            if command == "M":
                command = "L"
            index += 2
        else:
            index += 1
    if current:
        polygons.append(current)
    return polygons


def _ensure_cairo_runtime() -> None:
    homebrew_lib = "/opt/homebrew/lib"
    existing = os.environ.get("DYLD_FALLBACK_LIBRARY_PATH", "")
    if homebrew_lib not in existing.split(":"):
        os.environ["DYLD_FALLBACK_LIBRARY_PATH"] = f"{homebrew_lib}:{existing}" if existing else homebrew_lib


def _render_svg_with_cairosvg(svg: str, width: int, height: int, *, background_color: str | None) -> Image.Image:
    _ensure_cairo_runtime()
    import cairosvg  # type: ignore[import-not-found]

    kwargs: dict[str, object] = {
        "bytestring": svg.encode("utf-8"),
        "output_width": width,
        "output_height": height,
    }
    if background_color is not None:
        kwargs["background_color"] = background_color
    png_bytes = cairosvg.svg2png(**kwargs)
    return Image.open(io.BytesIO(png_bytes)).convert("RGBA")


def _render_lossless_runs_to_luma(svg: str, width: int, height: int) -> Image.Image:
    bitmap = np.zeros((height, width), dtype=bool)
    match = re.search(r'<path[^>]*\sd="([^"]*)"', svg)
    if match:
        # Our lossless path format is a list of one-pixel-high rectangles:
        # M x0 y L x1 y L x1 y+1 L x0 y+1 Z
        pattern = re.compile(r"M (\d+) (\d+) L (\d+) \2 L \3 (\d+) L \1 \4 Z")
        for run in pattern.finditer(match.group(1)):
            x0, y, x1, y_next = map(int, run.groups())
            if y_next == y + 1 and 0 <= y < height:
                bitmap[y, max(0, x0):min(width, x1)] = True
    return Image.fromarray(np.where(bitmap, 0, 255).astype(np.uint8), "L")


def render_svg_to_png(svg: str, width: int, height: int) -> Image.Image:
    """Rasterize SVG to a white-background grayscale PNG for quality scoring."""
    if 'data-trace-mode="lossless-runs"' in svg:
        return _render_lossless_runs_to_luma(svg, width, height)
    try:
        rendered = _render_svg_with_cairosvg(svg, width, height, background_color="white")
        return rendered.convert("L")
    except Exception:
        pass

    scale = 1
    mask = Image.new("1", (width * scale, height * scale), 0)
    from PIL import ImageDraw

    for polygon in _parse_own_path_polygons(svg):
        if len(polygon) < 3:
            continue
        poly_mask = Image.new("1", mask.size, 0)
        draw = ImageDraw.Draw(poly_mask)
        draw.polygon([(x * scale, y * scale) for x, y in polygon], fill=1)
        mask = ImageChops.logical_xor(mask, poly_mask)
    gray = mask.convert("L").resize((width, height), Image.Resampling.NEAREST)
    return Image.eval(gray, lambda value: 0 if value > 0 else 255)


def _svg_declared_size(svg: str) -> tuple[int, int]:
    viewbox = re.search(r'viewBox="\s*[-0-9.]+\s+[-0-9.]+\s+([0-9.]+)\s+([0-9.]+)\s*"', svg)
    if viewbox:
        return max(1, int(float(viewbox.group(1)))), max(1, int(float(viewbox.group(2))))
    width = re.search(r'\swidth="([0-9.]+)', svg)
    height = re.search(r'\sheight="([0-9.]+)', svg)
    if width and height:
        return max(1, int(float(width.group(1)))), max(1, int(float(height.group(1))))
    return 500, 500


def render_svg_to_product_png(svg: str, *, size: int = 500, source_width: int | None = None, source_height: int | None = None) -> Image.Image:
    """Render a transparent, square product PNG from an SVG without distorting aspect ratio."""
    source_width, source_height = (source_width, source_height) if source_width and source_height else _svg_declared_size(svg)
    try:
        if 'data-trace-mode="lossless-runs"' in svg:
            luma = _render_lossless_runs_to_luma(svg, int(source_width), int(source_height))
            alpha = Image.eval(luma, lambda value: 255 - value)
            rendered = Image.new("RGBA", luma.size, (0, 0, 0, 255))
            rendered.putalpha(alpha)
        else:
            rendered = _render_svg_with_cairosvg(svg, int(source_width), int(source_height), background_color=None)
    except Exception:
        luma = render_svg_to_png(svg, int(source_width), int(source_height))
        alpha = Image.eval(luma, lambda value: 255 - value)
        rendered = Image.new("RGBA", luma.size, (0, 0, 0, 0))
        rendered.putalpha(alpha)
    if rendered.getbbox() is None:
        return Image.new("RGBA", (size, size), (0, 0, 0, 0))
    scale = min(size / rendered.width, size / rendered.height)
    target = (max(1, round(rendered.width * scale)), max(1, round(rendered.height * scale)))
    rendered = rendered.resize(target, Image.Resampling.LANCZOS)
    canvas = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    canvas.alpha_composite(rendered, ((size - rendered.width) // 2, (size - rendered.height) // 2))
    return canvas


def _binary_foreground(image: Image.Image) -> np.ndarray:
    gray = np.asarray(image.convert("L"), dtype=np.uint8)
    return gray < 128


def compare_images(reference: Image.Image, rendered: Image.Image) -> SimilarityScore:
    if reference.size != rendered.size:
        rendered = rendered.resize(reference.size, Image.Resampling.LANCZOS)
    ref = np.asarray(reference.convert("L"), dtype=np.float32) / 255.0
    out = np.asarray(rendered.convert("L"), dtype=np.float32) / 255.0
    if ref.shape[0] < 7 or ref.shape[1] < 7:
        ssim = 1.0 - float(np.mean(np.abs(ref - out)))
    else:
        ssim = float(structural_similarity(ref, out, data_range=1.0))
    ref_fg = ref < 0.5
    out_fg = out < 0.5
    union = np.logical_or(ref_fg, out_fg).sum()
    intersection = np.logical_and(ref_fg, out_fg).sum()
    iou = 1.0 if union == 0 else float(intersection / union)
    abs_error = np.abs(ref - out)
    return SimilarityScore(
        ssim=ssim,
        foreground_iou=iou,
        mean_abs_error=float(abs_error.mean()),
        pixel_error_ratio=float((abs_error > 0.08).mean()),
    )


def mask_to_reference_image(mask: np.ndarray) -> Image.Image:
    return Image.fromarray(np.where(mask, 0, 255).astype(np.uint8), "L")


def save_diff(reference: Image.Image, rendered: Image.Image, path: Path) -> None:
    if reference.size != rendered.size:
        rendered = rendered.resize(reference.size, Image.Resampling.LANCZOS)
    diff = ImageChops.difference(reference.convert("L"), rendered.convert("L"))
    amplified = diff.point(lambda value: min(255, value * 5)).convert("RGB")
    path.parent.mkdir(parents=True, exist_ok=True)
    amplified.save(path)


def make_contact_sheet(rows: Iterable[tuple[str, Image.Image, Image.Image, Image.Image]], output_path: Path) -> None:
    rows = list(rows)
    if not rows:
        return
    tile = 120
    label_h = 24
    columns = 4
    sheet = Image.new("RGB", (columns * tile, len(rows) * (tile + label_h)), "white")
    from PIL import ImageDraw

    draw = ImageDraw.Draw(sheet)
    for row_index, (label, original, rendered, diff) in enumerate(rows):
        y = row_index * (tile + label_h)
        draw.text((4, y + 4), label, fill="black")
        for col, image in enumerate([original, rendered, diff]):
            thumb = image.convert("RGB")
            thumb.thumbnail((tile - 10, tile - 10), Image.Resampling.LANCZOS)
            x = (col + 1) * tile + (tile - thumb.width) // 2
            sheet.paste(thumb, (x, y + label_h + (tile - thumb.height) // 2))
    output_path.parent.mkdir(parents=True, exist_ok=True)
    sheet.save(output_path)
