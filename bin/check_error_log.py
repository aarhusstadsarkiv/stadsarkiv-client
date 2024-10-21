import sqlite3
import httpx
import time

db_file_path = "data/logs/errors.db"


def get_unresolved_urls():
    """Fetch all unresolved errors from the database."""
    conn = sqlite3.connect(db_file_path)
    cursor = conn.cursor()

    cursor.execute("SELECT id, url, error FROM error_logs WHERE resolved = 0")
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
print("Checking...")
print("-" * 50)

# Check the status of each unresolved URL
for error_id, url, error in unresolved_errors:

    if error == "404 Not Found":
        print("404 Not Found")
        mark_url_resolved(error_id)
        print("URL is now marked as resolved")
        print("-" * 50)
        continue

    print(url)
    print(f"Error: {error}")

    url = url.strip()
    http_status_code = check_url(url)

    print(f"Current status code: {http_status_code}")

    # get error code from error message
    error_code = error.split(" ")[0]

    # check if error code is 5xx
    if error_code.startswith("5") or error_code.startswith("4"):

        # If the URL has an accepted status - mark it as resolved
        resolved_statuses = [200, 301, 302, 400, 404]
        if http_status_code in resolved_statuses:
            mark_url_resolved(error_id)
            print("URL is now marked as resolved")
        else:
            print("URL is still unresolved")
    else:
        print("URL is still unresolved. Error is not a 500 Error")

    print("-" * 50)
    time.sleep(1)
