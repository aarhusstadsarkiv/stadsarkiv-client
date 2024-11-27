#!/usr/bin/env python
"""

Adds option for uses ordering materials from the archive to create the database tables.

export CONFIG_DIR=example-config-aarhus
./bin/orders.py

"""

from stadsarkiv_client.core.dynamic_settings import settings
from stadsarkiv_client.core.migration import Migration
from stadsarkiv_client.core.logging import get_log
import os

# Check if the environment variable CONFIG_DIR is set
if "CONFIG_DIR" not in os.environ:
    print("Environment variable CONFIG_DIR is not set. E.g. set it like this:")
    print("export CONFIG_DIR=example-config-aarhus")
    exit(1)

log = get_log()

create_orders_query = """
CREATE TABLE orders (
    order_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_email TEXT NOT NULL,
    user_display_name TEXT NOT NULL,
    user_id TEXT NOT NULL,
    label TEXT NOT NULL,
    resources TEXT,
    record_id TEXT NOT NULL,
    status INTEGER NOT NULL,
    deadline TEXT,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
    updated_at TEXT DEFAULT CURRENT_TIMESTAMP,
    finished INTEGER DEFAULT 0
) STRICT;

CREATE TABLE order_status_log (
    log_id INTEGER PRIMARY KEY AUTOINCREMENT,
    order_id INTEGER NOT NULL,
    status  INTEGER NOT NULL,
    changed_at TEXT DEFAULT CURRENT_TIMESTAMP,
    changed_by TEXT,
    FOREIGN KEY (order_id) REFERENCES orders(order_id)
) STRICT;

-- Index for looking up orders by record_id
CREATE INDEX idx_orders_record_id ON orders (record_id);

-- Index for looking up orders by status
CREATE INDEX idx_orders_status ON orders (status);

-- Index for queries involving deadlines
CREATE INDEX idx_orders_deadline ON orders (deadline);

-- Index for looking up status logs by order_id
CREATE INDEX idx_order_status_log_order_id ON order_status_log (order_id);

-- Index for filtering logs by status
CREATE INDEX idx_order_status_log_status ON order_status_log (status);

-- Index for logs sorted by change timestamp
CREATE INDEX idx_order_status_log_changed_at ON order_status_log (changed_at);

"""

# List of migrations with keys
migrations = {
    "create_orders": create_orders_query,
}

try:
    db_path = settings["sqlite3"]["orders"]
except KeyError:
    log.error("No database URL found in settings")
    exit(1)

migration_manager = Migration(db_path, migrations)
migration_manager.run_migrations()
migration_manager.close()
