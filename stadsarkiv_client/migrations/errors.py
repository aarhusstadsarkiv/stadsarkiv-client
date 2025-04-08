create_error_log = """
CREATE TABLE error_log (
    error_log_id INTEGER PRIMARY KEY AUTOINCREMENT,
    time TEXT,
    name TEXT,
    level TEXT,
    message TEXT,
    exception TEXT,
    url TEXT,
    error_code INTEGER,
    resolved INTEGER DEFAULT 0,
    UNIQUE(url, message)
) STRICT;

CREATE INDEX idx_time ON error_log (time);
CREATE INDEX idx_resolved ON error_log (resolved);
CREATE INDEX idx_error_code ON error_log (error_code);
CREATE INDEX idx_url ON error_log (url);
CREATE INDEX idx_message ON error_log (message);
"""

# List of migrations with keys
migrations_error_log = {
    "create_error_log": create_error_log,
}
