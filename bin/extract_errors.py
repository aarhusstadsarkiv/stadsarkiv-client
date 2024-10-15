"""
This script extracts error logs from log files and inserts them into a SQLite database.
"""

import re
import glob
import sqlite3

log_file_pattern = "/home/dennis/logs/main*"
db_file_path = "data/logs/errors.db"
change_host = "http://localhost:5555"

error_pattern = re.compile(r"(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2},\d{3}) - main - ERROR - 500 Error: (https?://[^\s]+)")

# Connect to the SQLite database (or create it if it doesn't exist)
conn = sqlite3.connect(db_file_path)
cursor = conn.cursor()

# Create the table if it doesn't exist
cursor.execute(
    """
    CREATE TABLE IF NOT EXISTS error_logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        url TEXT UNIQUE,
        error TEXT,
        resolved BOOLEAN DEFAULT 0
    )
"""
)
conn.commit()

# Find all files matching the pattern
log_files = glob.glob(log_file_pattern)

for log_file_path in log_files:
    with open(log_file_path, "r") as log_file:
        for line in log_file:
            match = error_pattern.search(line)
            if match:
                timestamp, original_url = match.groups()
                new_url = re.sub(r"https?://[^/]+", change_host, original_url)
                error_message = f"{timestamp} - main - ERROR - 500 Error: {new_url}"

                # Check if the URL already exists in the database
                cursor.execute("SELECT * FROM error_logs WHERE url = ?", (new_url,))
                result = cursor.fetchone()

                # If URL doesn't exist, insert it with resolved set to False
                if result is None:
                    cursor.execute("INSERT INTO error_logs (url, error, resolved) VALUES (?, ?, ?)", (new_url, error_message, False))
                    conn.commit()

# Close the database connection
conn.close()
