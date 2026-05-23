from __future__ import annotations

import hmac
import secrets
from hashlib import sha256


def generate_download_token() -> str:
    return secrets.token_urlsafe(32)


def hash_download_token(token: str, secret: str) -> str:
    digest = hmac.new(secret.encode("utf-8"), token.encode("utf-8"), sha256).hexdigest()
    return f"sha256:{digest}"
