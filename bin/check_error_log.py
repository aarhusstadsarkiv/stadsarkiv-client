import httpx

# allow to sleep
import time

urls_file = "data/logs/error_urls.txt"

# read the urls from the file
with open(urls_file, "r") as f:
    urls = f.readlines()

# print number of urls
num_urls = len(urls)
print(f"Found {num_urls} urls")

# remove duplicates
urls = list(set(urls))

# print number of unique urls
num_unique_urls = len(urls)
print(f"Found {num_unique_urls} unique urls")


def check_url(url):
    try:
        response = httpx.get(url)
        return response.status_code
    except httpx.RequestError:
        return "Request error"
    except httpx.HTTPStatusError:
        return "HTTP status error"


# check each url
for url in urls:
    url = url.strip()
    status = check_url(url)
    print(f"{url} - {status}")
    time.sleep(2)
