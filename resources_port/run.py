import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))  # noqa

from stadsarkiv_client.core.dynamic_settings import settings
from stadsarkiv_client.core.logging import get_log
from resources_port import api_port

import typing
import asyncio
import json


log = get_log()
base_url = str(settings["api_base_url"])
token = os.getenv("TOKEN")

if not token:
    raise Exception("No token. Set TOKEN environment variable")


# skema: address: http://localhost:5555/locations/15815/json/api
# skema: place: http://localhost:5555/locations/2335/json/api
# Max: 000159827

# resource_type = "locations"
# id = "2335"


def save_resource(id, resource):
    with open(f"resources/{id}.json", "w") as f:
        json.dump(resource, f, indent=4, ensure_ascii=False)


def resource_exists(id):
    return os.path.isfile(f"resources/{id}.json")


def utf8_fix(resource):
    # convert to string
    resource = json.dumps(resource)

    # replace as resource was a single string
    resource = resource.replace("\u00f8", "ø")
    resource = resource.replace("\u00e5", "å")
    resource = resource.replace("\u00e6", "æ")

    # convert back to json
    resource = json.loads(resource)
    return resource


max_resources = 159827
max_resources = 10


async def main():
    max_id = 159827
    resource_type = "locations"  # type does not matter
    id = 2335

    count = 0
    while id != max_id:
        if resource_exists(id):
            log.info(f"Resource {id} exists")
            id = id + 1
            continue

        log.debug(f"Getting resource {id}")
        # Assuming proxies_get_resource is an async function and type, id are defined
        try:
            resource = await api_port.proxies_get_resource(type=resource_type, id=str(id))
            resource = utf8_fix(resource)
            save_resource(id, resource)
        except Exception as e:
            log.exception(e)
            id = id + 1
            continue

        id = id + 1
        count = count + 1

        if count > max_resources:
            break


# Run the async main function
asyncio.run(main())
