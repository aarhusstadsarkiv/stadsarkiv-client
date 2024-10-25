import re
import glob
import sqlite3
import json

log_file_pattern = "/home/dennis/logs/main.log"
db_file_path = "./data/logs/errors.db"
change_host = "http://localhost:5555"

# Connect to the SQLite database
conn = sqlite3.connect(db_file_path)
cursor = conn.cursor()

# Create the table if it doesn't exist
cursor.execute(
    """
    CREATE TABLE IF NOT EXISTS error_logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        url TEXT,
        error TEXT,
        error_code INTEGER,
        exception TEXT,
        resolved BOOLEAN DEFAULT 0,
        UNIQUE(url, error)
    )
"""
)
conn.commit()

# Find all files matching the pattern
log_files = glob.glob(log_file_pattern)


def parse_line(line: str):
    log_data = json.loads(line)

    # Check if the log line is an error log
    if log_data.get("level") == "ERROR":
        error_message = log_data.get("message")
        error_code = log_data.get("error_code")
        original_url = log_data.get("request_url", "")
        exception = log_data.get("exception", "")

        new_url = re.sub(r"https?://[^/]+", change_host, original_url)

        # Check if combination exists
        cursor.execute("SELECT 1 FROM error_logs WHERE url = ? AND error = ?", (new_url, error_message))
        result = cursor.fetchone()

        # Insert the error into the database if it doesn't exist
        if result is None:
            cursor.execute(
                "INSERT INTO error_logs (url, error, error_code, exception, resolved) VALUES (?, ?, ?, ?, ?)",
                (new_url, error_message, error_code, exception, False),
            )
            conn.commit()


def parse_log_file(log_file_path: str):
    with open(log_file_path, "r") as log_file:
        for line in log_file:
            parse_line(line)


for log_file_path in log_files:
    parse_log_file(log_file_path)


conn.close()
