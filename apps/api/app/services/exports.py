from __future__ import annotations

import json
import re
import zipfile
from dataclasses import dataclass
from hashlib import sha256
from pathlib import Path
from time import time

from glyph_core import export_png, generate_glyph_set, render_svg
from glyph_core.manifest import build_manifest

from app.schemas import ExportRequest
from app.services.glyphs import make_spec
from app.settings import Settings

SAFE_NAME = re.compile(r"[^a-zA-Z0-9_.-]+")


@dataclass(frozen=True)
class ExportResult:
    export_id: str
    storage_path: Path
    manifest_path: Path
    zip_path: Path
    svg_paths: list[Path]
    png_paths: list[Path]


def _safe_filename(value: str) -> str:
    return SAFE_NAME.sub("-", value).strip("-") or "glyph"


def _coerce_request(payload: dict | ExportRequest) -> ExportRequest:
    if isinstance(payload, ExportRequest):
        return payload
    return ExportRequest.model_validate(payload)


def export_glyph_bundle(payload: dict | ExportRequest, settings: Settings | None = None) -> ExportResult:
    settings = settings or Settings()
    request = _coerce_request(payload)
    spec = make_spec(request)
    glyph_set = generate_glyph_set(spec)

    digest = sha256(f"{spec.stable_json()}|{time()}".encode("utf-8")).hexdigest()[:16]
    export_id = f"exp_{digest}"
    export_dir = settings.storage_root / export_id
    export_dir.mkdir(parents=True, exist_ok=False)

    svg_paths: list[Path] = []
    png_paths: list[Path] = []
    for glyph in glyph_set.glyphs:
        filename_root = f"{glyph.id}-{_safe_filename(glyph.name)}"
        svg = render_svg(glyph, spec)
        svg_path = export_dir / f"{filename_root}.svg"
        png_path = export_dir / f"{filename_root}-{request.png_size}.png"
        svg_path.write_text(svg, encoding="utf-8")
        png_path.write_bytes(export_png(svg, size=request.png_size, background=request.background))
        svg_paths.append(svg_path)
        png_paths.append(png_path)

    manifest = build_manifest(glyph_set, spec)
    manifest.update(
        {
            "exportId": export_id,
            "pngSize": request.png_size,
            "files": [path.name for path in [*svg_paths, *png_paths]],
        }
    )
    manifest_path = export_dir / "manifest.json"
    manifest_path.write_text(json.dumps(manifest, indent=2, sort_keys=True), encoding="utf-8")

    zip_path = export_dir / f"{export_id}.zip"
    with zipfile.ZipFile(zip_path, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        for path in [*svg_paths, *png_paths, manifest_path]:
            archive.write(path, arcname=path.name)

    return ExportResult(
        export_id=export_id,
        storage_path=export_dir,
        manifest_path=manifest_path,
        zip_path=zip_path,
        svg_paths=svg_paths,
        png_paths=png_paths,
    )
