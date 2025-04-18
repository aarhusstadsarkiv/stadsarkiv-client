#!/usr/bin/env python
"""
Check the error log added to the database for unresolved errors.
export CONFIG_DIR=example-config-aarhus
"""

from stadsarkiv_client.core.dynamic_settings import settings
import httpx
import time
import os
from stadsarkiv_client.database.utils import DatabaseConnection

# Check if the environment variable CONFIG_DIR is set
if "CONFIG_DIR" not in os.environ:
    print("Environment variable CONFIG_DIR is not set. E.g. set it like this:")
    print("export CONFIG_DIR=example-config-aarhus")
    exit(1)

# check if environment variable CONFIG_DIR is set


database_url = settings["sqlite3"]["errors"]
database_connection = DatabaseConnection(database_url)
transaction_scope_sync = database_connection.transaction_scope_sync

should_not_resolve = [
    "Representations but no record_type",
    "JSON Error in Agenda Item",
    "Sejrs sedler should have a summary",
    "Missing Image",
]

should_resolve = [
    "Error in _get_record_pagination",
]


def get_unresolved_urls():

    with transaction_scope_sync() as connection:
        cursor = connection.execute("SELECT * FROM error_log WHERE resolved = 0")
        unresolved_errors = cursor.fetchall()
        return unresolved_errors


def mark_url_resolved(error_log_id):
    """Mark the URL as resolved in the database."""

    with transaction_scope_sync() as connection:
        connection.execute("UPDATE error_log SET resolved = 1 WHERE error_log_id = ?", (error_log_id,))
        connection.commit()


def ignore_error_by_message(message):
    """
    Check if part of the message matches any of the strings in should_not_resolve.
    """
    for string in should_not_resolve:
        if string in message:
            return True
    return False


def resolve_error_by_message(message):
    """
    Check if part of the message matches any of the strings in should_resolve.
    """
    for string in should_resolve:
        if string in message:
            return True
    return False


def check_url(url):
    """Check the status of a URL."""
    response = httpx.get(url)
    return response.status_code


unresolved_errors = get_unresolved_urls()
num_unresolved = len(unresolved_errors)
print(f"Found {num_unresolved} unresolved URLs")
print("-" * 50)

# Iterate over each row as a dictionary-like object
for row in unresolved_errors:

    error_log_id = row["error_log_id"]
    url = row["url"]
    message = row["message"]
    error_code = row["error_code"]

    url = url.strip()
    current_status_code = ""
    resolution = "Unresolved"

    if ignore_error_by_message(message):
        resolution = "Ignored"

    elif resolve_error_by_message(message):
        mark_url_resolved(error_log_id)
        resolution = "Resolved"

    elif url:
        try:
            http_status_code = check_url(url)
            current_status_code = f"{http_status_code}"
        except Exception as e:
            print(e)
            continue

        # Check if the error is resolvable
        # if http_status_code >= 400 and http_status_code < 500:
        resolved_statuses = [200, 301, 302, 400, 404, 422]
        if http_status_code in resolved_statuses:
            mark_url_resolved(error_log_id)
            resolution = "Resolved"

    else:
        resolution = "Ignored. No URL"

    # Print information for the current URL, with URL on one line
    print(f"ID: {error_log_id}")
    print(f"URL: {url}")
    print(f"Error Message: {message}")
    print(f"Error Code: {error_code}")
    print(f"Current Status: {current_status_code}")
    print(f"Resolution: {resolution}")
    print("-" * 50)

    # Pause for a second between requests
    time.sleep(0.1)
