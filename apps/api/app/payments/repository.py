from __future__ import annotations

import json
import sqlite3
from dataclasses import dataclass
from pathlib import Path
from time import time
from typing import Any

from app.payments.downloads import generate_download_token, hash_download_token
from app.settings import Settings


@dataclass(frozen=True)
class OrderRecord:
    id: str
    status: str
    checkout_session_id: str
    amount_cents: int
    currency: str
    customer_email: str | None
    spec_json: str
    export_id: str | None
    export_zip_path: str | None
    download_token_hash: str | None
    download_token_expires_at: int | None
    created_at: int
    updated_at: int

    @property
    def download_token_plaintext(self) -> None:
        return None

    def spec_payload(self) -> dict[str, Any]:
        return json.loads(self.spec_json)


class PaymentRepository:
    def __init__(self, db_path: Path):
        self.db_path = db_path
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._init_schema()

    def _connect(self) -> sqlite3.Connection:
        connection = sqlite3.connect(self.db_path)
        connection.row_factory = sqlite3.Row
        return connection

    def _init_schema(self) -> None:
        with self._connect() as connection:
            connection.execute(
                """
                CREATE TABLE IF NOT EXISTS orders (
                  id TEXT PRIMARY KEY,
                  status TEXT NOT NULL CHECK(status IN ('pending', 'paid', 'expired', 'cancelled')),
                  checkout_session_id TEXT NOT NULL UNIQUE,
                  amount_cents INTEGER NOT NULL,
                  currency TEXT NOT NULL,
                  customer_email TEXT,
                  spec_json TEXT NOT NULL,
                  export_id TEXT,
                  export_zip_path TEXT,
                  download_token_hash TEXT,
                  download_token_expires_at INTEGER,
                  created_at INTEGER NOT NULL,
                  updated_at INTEGER NOT NULL
                )
                """
            )
            connection.execute(
                """
                CREATE TABLE IF NOT EXISTS webhook_events (
                  id TEXT PRIMARY KEY,
                  type TEXT NOT NULL,
                  received_at INTEGER NOT NULL
                )
                """
            )

    @staticmethod
    def _row_to_order(row: sqlite3.Row | None) -> OrderRecord | None:
        if row is None:
            return None
        return OrderRecord(**dict(row))

    def create_order(
        self,
        *,
        order_id: str,
        checkout_session_id: str,
        amount_cents: int,
        currency: str,
        customer_email: str | None,
        spec_payload: dict[str, Any],
    ) -> OrderRecord:
        now = int(time())
        with self._connect() as connection:
            connection.execute(
                """
                INSERT INTO orders (
                  id, status, checkout_session_id, amount_cents, currency, customer_email,
                  spec_json, created_at, updated_at
                ) VALUES (?, 'pending', ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    order_id,
                    checkout_session_id,
                    amount_cents,
                    currency,
                    customer_email,
                    json.dumps(spec_payload, sort_keys=True, separators=(",", ":")),
                    now,
                    now,
                ),
            )
        order = self.get_order(order_id)
        assert order is not None
        return order

    def get_order(self, order_id: str) -> OrderRecord | None:
        with self._connect() as connection:
            row = connection.execute("SELECT * FROM orders WHERE id = ?", (order_id,)).fetchone()
        return self._row_to_order(row)

    def get_order_by_session(self, checkout_session_id: str) -> OrderRecord | None:
        with self._connect() as connection:
            row = connection.execute("SELECT * FROM orders WHERE checkout_session_id = ?", (checkout_session_id,)).fetchone()
        return self._row_to_order(row)

    def record_webhook_once(self, event_id: str, event_type: str) -> bool:
        try:
            with self._connect() as connection:
                connection.execute(
                    "INSERT INTO webhook_events (id, type, received_at) VALUES (?, ?, ?)",
                    (event_id, event_type, int(time())),
                )
        except sqlite3.IntegrityError:
            return False
        return True

    def mark_paid(self, order_id: str, *, export_id: str, export_zip_path: Path, settings: Settings) -> str:
        token = generate_download_token()
        token_hash = hash_download_token(token, settings.download_token_secret)
        expires_at = int(time()) + settings.download_token_ttl_seconds
        with self._connect() as connection:
            connection.execute(
                """
                UPDATE orders
                   SET status = 'paid', export_id = ?, export_zip_path = ?,
                       download_token_hash = ?, download_token_expires_at = ?, updated_at = ?
                 WHERE id = ? AND status IN ('pending', 'paid')
                """,
                (export_id, str(export_zip_path), token_hash, expires_at, int(time()), order_id),
            )
        return token

    def issue_download_token(self, order_id: str, *, settings: Settings) -> str:
        order = self.get_order(order_id)
        if order is None or order.status != "paid" or order.export_zip_path is None:
            raise ValueError("download token can only be issued for a paid exported order")
        token = generate_download_token()
        token_hash = hash_download_token(token, settings.download_token_secret)
        expires_at = int(time()) + settings.download_token_ttl_seconds
        with self._connect() as connection:
            connection.execute(
                """
                UPDATE orders
                   SET download_token_hash = ?, download_token_expires_at = ?, updated_at = ?
                 WHERE id = ? AND status = 'paid'
                """,
                (token_hash, expires_at, int(time()), order_id),
            )
        return token

    def get_paid_order_by_download_token(self, token: str, *, settings: Settings) -> OrderRecord | None:
        token_hash = hash_download_token(token, settings.download_token_secret)
        with self._connect() as connection:
            row = connection.execute(
                """
                SELECT * FROM orders
                 WHERE status = 'paid'
                   AND download_token_hash = ?
                   AND download_token_expires_at > ?
                """,
                (token_hash, int(time())),
            ).fetchone()
        return self._row_to_order(row)
