from __future__ import annotations

import hashlib
import json
import re
from dataclasses import asdict, dataclass, field
from typing import Any

ALLOWED_STYLES = {
    "minimal",
    "tech",
    "premium-ui",
    "geometric",
    "mystic",
    "organic",
    "dashboard",
}
ALLOWED_COMPLEXITIES = {"simple", "balanced", "dense"}
MAX_GLYPH_COUNT = 64
HEX_COLOR_RE = re.compile(r"^#[0-9a-fA-F]{6}([0-9a-fA-F]{2})?$")


def validate_color(value: str | None, field_name: str) -> None:
    if value is None:
        return
    if value == "currentColor":
        return
    if not HEX_COLOR_RE.match(value):
        raise ValueError(f"{field_name} must be a hex color like #9d9788")


@dataclass(frozen=True)
class Palette:
    stroke: str = "#111827"
    background: str | None = None

    def __post_init__(self) -> None:
        validate_color(self.stroke, "stroke color")
        validate_color(self.background, "background color")

    def to_dict(self) -> dict[str, str | None]:
        return {"stroke": self.stroke, "background": self.background}


@dataclass(frozen=True)
class GlyphGenerationSpec:
    seed: str
    count: int = 24
    style: str = "premium-ui"
    complexity: str = "balanced"
    stroke_width: float = 2.0
    palette: Palette = field(default_factory=Palette)
    background: str | None = None
    view_box: str = "0 0 48 48"
    motif_families: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        if not str(self.seed):
            raise ValueError("seed must not be empty")
        if self.style not in ALLOWED_STYLES:
            raise ValueError(f"style must be one of {sorted(ALLOWED_STYLES)}")
        if self.complexity not in ALLOWED_COMPLEXITIES:
            raise ValueError(f"complexity must be one of {sorted(ALLOWED_COMPLEXITIES)}")
        if not 1 <= self.count <= MAX_GLYPH_COUNT:
            raise ValueError(f"count must be between 1 and {MAX_GLYPH_COUNT}")
        if self.stroke_width <= 0:
            raise ValueError("stroke_width must be positive")
        validate_color(self.background, "background color")
        # Normalize motif_families to a tuple even if callers pass a list.
        object.__setattr__(self, "motif_families", tuple(self.motif_families))

    def to_dict(self) -> dict[str, Any]:
        data = asdict(self)
        data["palette"] = self.palette.to_dict()
        data["motif_families"] = list(self.motif_families)
        return data

    def stable_json(self) -> str:
        return json.dumps(self.to_dict(), sort_keys=True, separators=(",", ":"))

    def hash(self) -> str:
        digest = hashlib.sha256(self.stable_json().encode("utf-8")).hexdigest()
        return f"sha256:{digest}"


@dataclass(frozen=True)
class Glyph:
    id: str
    name: str
    elements: tuple[str, ...]
    template: str
    tags: tuple[str, ...] = ()

    @property
    def paths(self) -> tuple[dict[str, Any], ...]:
        # Compatibility slot for callers that want a structured field later.
        return tuple({"svg": element} for element in self.elements)


@dataclass(frozen=True)
class GlyphSet:
    spec_hash: str
    glyphs: tuple[Glyph, ...]
