from __future__ import annotations

import io
import zipfile
from pathlib import Path

from fastapi.testclient import TestClient
from PIL import Image

from app.main import app
from app.services.exports import export_glyph_bundle
from app.settings import Settings


client = TestClient(app)


def test_health_endpoint_reports_service_status() -> None:
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {
        "ok": True,
        "service": "vectorglyphs-api",
        "version": "0.1.0",
    }


def test_generate_endpoint_returns_deterministic_svg_previews() -> None:
    payload = {
        "seed": "phase-3-api",
        "count": 3,
        "style": "premium-ui",
        "complexity": "balanced",
        "stroke": "#9d9788",
        "background": None,
    }

    first = client.post("/api/generate", json=payload)
    second = client.post("/api/generate", json=payload)

    assert first.status_code == 200
    assert first.json() == second.json()
    body = first.json()
    assert body["specHash"].startswith("sha256:")
    assert len(body["glyphs"]) == 3
    assert body["glyphs"][0]["id"] == "glyph_001"
    assert body["glyphs"][0]["svg"].startswith("<svg")
    assert "<script" not in body["glyphs"][0]["svg"].lower()
    assert "href=" not in body["glyphs"][0]["svg"].lower()


def test_generate_endpoint_validates_input() -> None:
    response = client.post("/api/generate", json={"seed": "bad", "count": 0, "style": "premium-ui"})

    assert response.status_code == 422


def test_export_endpoint_writes_svg_png_zip_and_manifest(tmp_path: Path) -> None:
    payload = {
        "seed": "phase-3-export",
        "count": 2,
        "style": "dashboard",
        "complexity": "simple",
        "stroke": "#111827",
        "background": None,
        "pngSize": 512,
    }

    result = export_glyph_bundle(payload, settings=Settings(storage_root=tmp_path))

    assert result.export_id.startswith("exp_")
    assert result.storage_path.is_relative_to(tmp_path)
    assert result.manifest_path.exists()
    assert result.zip_path.exists()
    assert len(result.svg_paths) == 2
    assert len(result.png_paths) == 2

    png = Image.open(io.BytesIO(result.png_paths[0].read_bytes()))
    assert png.size == (512, 512)

    with zipfile.ZipFile(result.zip_path) as archive:
        names = set(archive.namelist())
    assert "manifest.json" in names
    assert any(name.endswith(".svg") for name in names)
    assert any(name.endswith("-512.png") for name in names)


def test_export_endpoint_returns_bundle_metadata() -> None:
    payload = {
        "seed": "phase-3-export-endpoint",
        "count": 1,
        "style": "minimal",
        "complexity": "simple",
        "stroke": "#111827",
        "background": None,
        "pngSize": 512,
    }

    response = client.post("/api/export", json=payload)

    assert response.status_code == 200
    body = response.json()
    assert body["exportId"].startswith("exp_")
    assert body["format"] == "zip"
    assert body["fileCount"] == 4  # SVG + PNG + manifest + ZIP
    assert body["zipFile"].endswith(".zip")
    assert body["expiresInSeconds"] == 3600
