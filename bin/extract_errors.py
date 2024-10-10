import re

log_file_path = "data/logs/main.log"
output_file_path = "data/logs/extracted.log"
url_list_path = "data/logs/error_urls.txt"

change_host = "http://localhost:5555"

error_pattern = re.compile(r"(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2},\d{3}) - main - ERROR - 500 Error: (https?://[^\s]+)")

with open(log_file_path, "r") as log_file, open(output_file_path, "w") as output_file, open(url_list_path, "w") as url_file:

    for line in log_file:
        match = error_pattern.search(line)
        if match:
            timestamp, original_url = match.groups()
            new_url = re.sub(r"https?://[^/]+", change_host, original_url)

            updated_line = f"{timestamp} - main - ERROR - 500 Error: {new_url}\n"
            output_file.write(updated_line)

            url_file.write(f"{new_url}\n")
