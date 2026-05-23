from __future__ import annotations

import re
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator

GlyphStyle = Literal["minimal", "tech", "premium-ui", "geometric", "mystic", "organic", "dashboard"]
GlyphComplexity = Literal["simple", "balanced", "dense"]
PngSize = Literal[512, 1024, 2048, 4096]
HEX_COLOR = re.compile(r"^#[0-9a-fA-F]{6}([0-9a-fA-F]{2})?$")


class GenerateRequest(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    seed: str = Field(min_length=1, max_length=128)
    count: int = Field(default=12, ge=1, le=64)
    style: GlyphStyle = "premium-ui"
    complexity: GlyphComplexity = "balanced"
    stroke: str = Field(default="#111827")
    background: str | None = None

    @field_validator("stroke", "background")
    @classmethod
    def validate_hex_color(cls, value: str | None) -> str | None:
        if value is None:
            return None
        if not HEX_COLOR.match(value):
            raise ValueError("color must be a hex color like #9d9788")
        return value


class ExportRequest(GenerateRequest):
    png_size: PngSize = Field(default=2048, alias="pngSize")


class CheckoutRequest(ExportRequest):
    customer_email: str | None = Field(default=None, alias="customerEmail")


class GlyphPreview(BaseModel):
    id: str
    name: str
    template: str
    tags: list[str]
    svg: str


class GenerateResponse(BaseModel):
    spec_hash: str = Field(alias="specHash")
    glyphs: list[GlyphPreview]


class ExportResponse(BaseModel):
    export_id: str = Field(alias="exportId")
    format: Literal["zip"] = "zip"
    file_count: int = Field(alias="fileCount")
    zip_file: str = Field(alias="zipFile")
    manifest_file: str = Field(alias="manifestFile")
    storage_path: str = Field(alias="storagePath")
    expires_in_seconds: int = Field(alias="expiresInSeconds")


class CheckoutResponse(BaseModel):
    order_id: str = Field(alias="orderId")
    status: Literal["pending"] = "pending"
    checkout_session_id: str = Field(alias="checkoutSessionId")
    checkout_url: str = Field(alias="checkoutUrl")
