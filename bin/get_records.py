import json
import httpx
from time import sleep
from stadsarkiv_client.core.dynamic_settings import init_settings
from stadsarkiv_client.core.logging import get_log

init_settings()
log = get_log()

# HOST = "http://localhost:5555"
HOST = "https://www.aarhusarkivet.dk"


# read all records from data/all_records.json
with open("./data/records_all.json", "r") as f:
    records_all: list = json.load(f)


def get_record(record_id):
    try:
        url = f"{HOST}/records/{record_id}"
        log.info(f"Visiting record: {url}")
        response = httpx.get(url)
        return response
    except httpx.ConnectError:
        return None
    except httpx.HTTPStatusError:
        # This is ok. connection has been made
        return True


# File where current record id is saved, eg. 1234
current_id_file = "./data/current_id.txt"

# If file does not exists, create it with 0
try:
    with open(current_id_file, "x") as f:
        f.write("0")
except FileExistsError:
    pass

# read current id from file
with open(current_id_file, "r") as f:
    current_id = int(f.read())


# Loop through all records and visit each record
for record_id in records_all[current_id:]:
    response = get_record(record_id)
    if response is None:
        log.error("Connection error. Exiting.")
        break

    sleep(0.5)

    # Save current id to file
    with open(current_id_file, "w") as f:
        f.write(str(current_id))
    current_id += 1
