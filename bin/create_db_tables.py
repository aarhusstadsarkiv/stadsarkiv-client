"""
stadsarkiv-client exec -c example-config-aarhus -s bin/create_db_tables.py
"""

from stadsarkiv_client.core.dynamic_settings import init_settings
import sqlite3
import os
from stadsarkiv_client.core.logging import get_log

init_settings()

log = get_log()

DATABASE_URL = str(os.getenv("DATABASE_URL"))
conn = sqlite3.connect(DATABASE_URL)
cursor = conn.cursor()

sql_statements = []

create_booksmarks_query = """
CREATE TABLE IF NOT EXISTS bookmarks (
    id INTEGER PRIMARY KEY,
    bookmark VARCHAR(128),
    user_id VARCHAR(128),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
"""

create_booksmarks_index_query = """
-- Generate index on user_id
CREATE INDEX idx_bookmarks_user_id ON bookmarks (user_id);
"""

create_searches_query = """
CREATE TABLE IF NOT EXISTS searches (
    id INTEGER PRIMARY KEY,
    search VARCHAR(1024),
    title VARCHAR(256),
    user_id VARCHAR(128),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
"""

create_searches_index_query = """
-- Generate index on user_id
CREATE INDEX idx_searches_user_id ON searches (user_id);
"""

create_cache_query = """
CREATE TABLE IF NOT EXISTS cache (
    id INTEGER PRIMARY KEY,
    key VARCHAR(128),
    value TEXT,
    unix_timestamp INTEGER DEFAULT 0
);
"""

create_cache_index_query = """
-- Generate index on key
CREATE INDEX idx_cache_key ON cache (key);
"""

sql_statements.append(create_booksmarks_query)
sql_statements.append(create_booksmarks_index_query)
sql_statements.append(create_searches_query)
sql_statements.append(create_searches_index_query)
sql_statements.append(create_cache_query)
sql_statements.append(create_cache_index_query)


# Create the table
def create_tables():
    for sql in sql_statements:
        cursor.execute(sql)
        conn.commit()
        log.debug("SQL executed")


create_tables()

conn.close()
