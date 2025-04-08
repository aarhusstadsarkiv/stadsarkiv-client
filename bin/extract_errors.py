#!/usr/bin/env python

from stadsarkiv_client.core.dynamic_settings import settings
from stadsarkiv_client.core.logging import get_log
import glob
import sqlite3
import json
import os
import argparse


# Check if the environment variable CONFIG_DIR is set
if "CONFIG_DIR" not in os.environ:
    print("Environment variable CONFIG_DIR is not set. E.g. set it like this:")
    print("export CONFIG_DIR=example-config-aarhus")
    exit(1)


log = get_log()

"""
We need a log file pattern to search for as a argument.
Otherwise, we will use the default log files at ./data/logs/main.log
"""


def parse_arguments():
    parser = argparse.ArgumentParser(description="Parse log files and extract error logs.")
    parser.add_argument(
        "--glob",
        type=str,
        default="./data/logs/main.log*",
        help="Path to the glob file pattern to use when extracting logs. Default: './data/logs/main.log*'",
    )
    return parser.parse_args()


args = parse_arguments()
log_file_pattern = args.glob

try:
    db_path = settings["sqlite3"]["errors"]
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

    # Only proceed if the log line is an ERROR log
    if log_data.get("level") == "ERROR":
        time = log_data.get("time")
        name = log_data.get("name")
        level = log_data.get("level")
        error_message = log_data.get("message")
        error_code = log_data.get("error_code", 0)
        request_url = log_data.get("request_url", "")
        exception = log_data.get("exception", "")

        # Check if combination exists
        cursor.execute("SELECT 1 FROM error_log WHERE url = ? AND message = ?", (request_url, error_message))
        result = cursor.fetchone()

        # Insert the error into the database if it doesn't exist
        if result is None:
            cursor.execute(
                """
                INSERT INTO error_log (time, name, level, message, exception, url, error_code, resolved)
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
    print(f"Processing log file: {log_file_path}")
    parse_log_file(log_file_path)

# Close the connection
conn.close()
