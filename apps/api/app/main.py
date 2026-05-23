from __future__ import annotations

from fastapi import FastAPI

from app.schemas import ExportRequest, ExportResponse, GenerateRequest, GenerateResponse
from app.services.exports import export_glyph_bundle
from app.services.glyphs import generate_preview_response
from app.settings import Settings

app = FastAPI(title="VectorGlyphs API", version="0.1.0")
settings = Settings()


@app.get("/health")
def health() -> dict[str, bool | str]:
    return {"ok": True, "service": "vectorglyphs-api", "version": "0.1.0"}


@app.post("/api/generate", response_model=GenerateResponse, response_model_by_alias=True)
def generate(request: GenerateRequest) -> GenerateResponse:
    return generate_preview_response(request)


@app.post("/api/export", response_model=ExportResponse, response_model_by_alias=True)
def export(request: ExportRequest) -> ExportResponse:
    result = export_glyph_bundle(request, settings=settings)
    return ExportResponse(
        exportId=result.export_id,
        fileCount=len(result.svg_paths) + len(result.png_paths) + 2,
        zipFile=result.zip_path.name,
        manifestFile=result.manifest_path.name,
        storagePath=str(result.storage_path),
        expiresInSeconds=settings.export_ttl_seconds,
    )
