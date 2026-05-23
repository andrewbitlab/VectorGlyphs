-- VectorGlyphs Phase 4 payment schema for future Postgres deployment.
-- The local Phase 4 API uses SQLite for safe local/test-mode execution; this DDL documents
-- the production-equivalent relational schema before Docker/Postgres is introduced.

CREATE TYPE order_status AS ENUM ('pending', 'paid', 'expired', 'cancelled');

CREATE TABLE IF NOT EXISTS orders (
  id TEXT PRIMARY KEY,
  status order_status NOT NULL DEFAULT 'pending',
  checkout_session_id TEXT NOT NULL UNIQUE,
  amount_cents INTEGER NOT NULL CHECK (amount_cents > 0),
  currency TEXT NOT NULL CHECK (char_length(currency) = 3),
  customer_email TEXT,
  spec_json JSONB NOT NULL,
  export_id TEXT,
  export_zip_path TEXT,
  download_token_hash TEXT,
  download_token_expires_at BIGINT,
  created_at BIGINT NOT NULL,
  updated_at BIGINT NOT NULL,
  CONSTRAINT paid_orders_have_exports CHECK (
    status <> 'paid' OR (export_id IS NOT NULL AND export_zip_path IS NOT NULL)
  )
);

CREATE INDEX IF NOT EXISTS idx_orders_status ON orders(status);
CREATE INDEX IF NOT EXISTS idx_orders_download_token_hash ON orders(download_token_hash);

CREATE TABLE IF NOT EXISTS webhook_events (
  id TEXT PRIMARY KEY,
  type TEXT NOT NULL,
  received_at BIGINT NOT NULL
);
