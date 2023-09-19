from urllib.parse import quote_plus
import httpx
import typing
import logging
from stadsarkiv_client.settings_query_params import settings_query_params

log = logging.getLogger(__name__)


def _get_resolve_records(records: list):
    """
    resolve collection and content_types from records. Return as list of tuples
    These are used to resolve content_types and collections present in the search result
    """
    resolve_records = []
    for record in records:
        if "collection_id" in record and record["collection_id"]:
            resolve_records.append(("collection", record["collection_id"]))
        if "content_types" in record:
            type = record["content_types"][-1]
            resolve_records.append(("content_types", type))

    return resolve_records


def _get_resource_types() -> list:
    """
    Get all resource types settings
    """
    resource_types = []
    for key, value in settings_query_params.items():
        if value.get("entity", False):
            resource_types.append(key)

    return resource_types


def _get_str_from_list(items: list) -> str:
    """
    Get list of tuples and return it as a quote plus encoded string.
    """
    query_str = ""
    for key, value in items:
        query_str += f"{key}={quote_plus(value)}&"

    return query_str


def _get_resolve_query_str(query_params: list, record_params: list):
    """ "
    Resolve query_params and extend list with record_params
    list is then converted to a query string to send to the aws API
    """
    resource_types = _get_resource_types()
    resolve_query_params = [(k, v) for k, v in query_params if k in resource_types]

    resolve_query_params.extend(record_params)
    resolve_query_params = list(set(resolve_query_params))

    resolve_query_string = _get_str_from_list(resolve_query_params)
    return resolve_query_string


async def _proxies_resolve(query_str) -> typing.Any:
    """resolve query params"""
    async with httpx.AsyncClient() as client:
        url = f"https://openaws.appspot.com/resolve_params?{query_str}"
        response = await client.get(url)
        if response.is_success:
            return response.json()["resolved_params"]
        else:
            response.raise_for_status()


async def set_resolved_search(search_result: dict, query_params: list) -> dict:
    result_params = _get_resolve_records(search_result["result"])
    resolve_query_str = _get_resolve_query_str(query_params, result_params)

    # Call endpoint to resolve
    facets_resolved = await _proxies_resolve(query_str=resolve_query_str)

    # Attach resolved facets to search result
    search_result["facets_resolved"] = facets_resolved

    return search_result
