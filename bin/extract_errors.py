from stadsarkiv_client.core.dynamic_settings import settings
from stadsarkiv_client.core.logging import get_log
import glob
import sqlite3
import json


log_file_pattern = "data/logs/main.log"
log = get_log()

try:
    db_path = settings["sqlite3"]["default"]
except KeyError:
    log.error("No database URL found in settings")
    exit(1)

# Connect to the SQLite database
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Find all files matching the pattern
log_files = glob.glob(log_file_pattern)


def parse_line(line: str):
    log_data = json.loads(line)

    # Only proceed if the log line is an error log
    if log_data.get("level") == "ERROR":
        time = log_data.get("time")
        name = log_data.get("name")
        level = log_data.get("level")
        error_message = log_data.get("message")
        error_code = log_data.get("error_code", 0)
        request_url = log_data.get("request_url", "")
        exception = log_data.get("exception", "")

        # Check if combination exists
        cursor.execute("SELECT 1 FROM error_logs WHERE url = ? AND message = ? AND time = ?", (request_url, error_message, time))
        result = cursor.fetchone()

        # Insert the error into the database if it doesn't exist
        if result is None:
            cursor.execute(
                """
                INSERT INTO error_logs (time, name, level, message, exception, url, error_code, resolved)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (time, name, level, error_message, exception, request_url, error_code, False),
            )
            conn.commit()


def parse_log_file(log_file_path: str):
    with open(log_file_path, "r") as log_file:
        for line in log_file:
            parse_line(line)


# Process each log file
for log_file_path in log_files:
    parse_log_file(log_file_path)

# Close the connection
conn.close()
