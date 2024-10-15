import sqlite3
import httpx
import time

db_file_path = "data/logs/errors.db"


def get_unresolved_urls():
    """Fetch all unresolved errors from the database."""
    conn = sqlite3.connect(db_file_path)
    cursor = conn.cursor()

    cursor.execute("SELECT id, url FROM error_logs WHERE resolved = 0")
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
    try:
        response = httpx.get(url)
        return response.status_code
    except httpx.RequestError:
        return "Request error"
    except httpx.HTTPStatusError:
        return "HTTP status error"


# Fetch unresolved URLs from the database
unresolved_errors = get_unresolved_urls()

# Print the number of unresolved URLs
num_unresolved = len(unresolved_errors)
print(f"Found {num_unresolved} unresolved URLs")

# Check the status of each unresolved URL
for error_id, url in unresolved_errors:
    url = url.strip()
    status = check_url(url)

    print(status)

    # If the URL is working (status code 200), mark it as resolved
    if status == 200:
        mark_url_resolved(error_id)
        print(f"{url} marked as resolved.")
    else:
        print(f"{url} is still unresolved.")

    # Sleep to avoid overwhelming the server
    time.sleep(2)
