import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))  # noqa

import httpx
from stadsarkiv_client.core.dynamic_settings import settings
from stadsarkiv_client.core.logging import get_log
from stadsarkiv_client.core import api

import typing


log = get_log()
base_url = str(settings["api_base_url"])


def _get_async_client() -> httpx.AsyncClient:
    return httpx.AsyncClient(timeout=7)


async def proxies_get_resource(type: str, id: str) -> typing.Any:
    async with _get_async_client() as client:
        url = base_url + f"/proxy/{type}/{id}"
        response = await client.get(url)

        if response.is_success:
            json = response.json()
            return json

        else:
            response.raise_for_status()


async def entity_post(json_data, schema_name) -> typing.Any:
    """
    POST entity to api
    Entity is a json dict with data and schema_name
    Endpoint will set latest version of schema
    """

    json_data = {"data": json_data, "schema_name": schema_name}

    access_token = "SOME_TOKEN"
    headers = {"Content-Type": "application/json", "Accept": "application/json", "Authorization": f"Bearer {access_token}"}

    url = base_url + "/entities/"

    async with _get_async_client() as client:
        response = await client.post(
            url=url,
            follow_redirects=True,
            headers=headers,
            json=json_data,
        )

        if response.is_success:
            return response.json()
        else:
            response.raise_for_status()


# skema: address: http://localhost:5555/locations/15815/json/api
# skema: place: http://localhost:5555/locations/2335/json/api
# Max: 000159827

# resource_type = "locations"
# id = "2335"
