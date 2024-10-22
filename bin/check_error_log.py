import sqlite3
import httpx
import time

db_file_path = "data/logs/errors.db"


def get_unresolved_urls():
    conn = sqlite3.connect(db_file_path)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM error_logs WHERE resolved = 0")
    unresolved_errors = cursor.fetchall()

    conn.close()

    return unresolved_errors


def mark_url_resolved(error_id):
    """Mark the URL as resolved in the database."""
    conn = sqlite3.connect(db_file_path)
    cursor = conn.cursor()

    cursor.execute("UPDATE error_logs SET resolved = 1 WHERE id = ?", (error_id,))
    conn.commit()

    conn.close()


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
    error_id = row["id"]
    url = row["url"]
    error = row["error"]
    error_code = row["error_code"]

    url = url.strip()
    current_status_code = ""
    resolution = "Unresolved"

    if error_code == "404":
        current_status_code = "404"
        mark_url_resolved(error_id)
        resolution = "Resolved"
    else:
        try:
            http_status_code = check_url(url)
            current_status_code = f"{http_status_code}"
        except Exception:
            # Ignore httpx exceptions
            continue

        # Check if the error is resolvable
        if http_status_code >= 400 and http_status_code < 600:
            resolved_statuses = [200, 301, 302, 400, 404]
            if http_status_code in resolved_statuses:
                mark_url_resolved(error_id)
                resolution = "Resolved"

    # Print information for the current URL, with URL on one line
    print(f"ID: {error_id}")
    print(f"URL: {url}")
    print(f"Error Message: {error}")
    print(f"Error Code: {error_code}")
    print(f"Status: {current_status_code}")
    print(f"Resolution: {resolution}")
    print("-" * 50)

    # Pause for a second between requests
    time.sleep(1)
