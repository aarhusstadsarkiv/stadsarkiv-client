"""
Normalize record data from the API to a more sane data structure
"""

from stadsarkiv_client.core.logging import get_log
import urllib.parse
from stadsarkiv_client.records.record_definitions import record_definitions
from stadsarkiv_client.core.dynamic_settings import settings
from stadsarkiv_client.core import cookie
from starlette.requests import Request


_search_base_url = settings["search_base_url"]
log = get_log()


search_query_params: list = []


def normalize_record_data(request: Request, record: dict, meta_data: dict):
    """
    Normalize record data to a more sane data structure
    """

    global search_query_params

    search_query_params = cookie.get_search_query_params(request)  # type: ignore

    record = _normalize_dict_data(record)
    record = _normalize_series(record)
    record = _normalize_content_types(record)
    record = _normalize_subjects(record)
    record = _normalize_labels(record)
    record = _normalize_resources(record)

    link_list = _get_list_of_type("link_list")
    link_list.remove("collection_tags")  # remove 'collection_tags' from link_list. This does not have an ID
    record = _normalize_link_lists(link_list, record)

    link_dict = _get_list_of_type("link_dict")
    record = _normalize_link_dicts(link_dict, record)

    record = _normalize_collection_tags(record)
    record = _normalize_representations(record, meta_data)

    return record


def _normalize_search_query(search_str: str):

    # copy search_query_params
    local_search_query_params = list(search_query_params)

    # get query part of the search string
    query_part = search_str.split("?")[1]

    # generate list of tuples from query_part
    query_list = []
    for query in query_part.split("&"):
        query_list.append(tuple(query.split("=")))

    # add to search_query_params any query that is not already in search_query_params
    for query in query_list:  # type: ignore
        if query not in local_search_query_params:
            local_search_query_params.append(query)

    # convert search_query_params to a string
    search_str = "/search?"
    for query in local_search_query_params:
        search_str += f"{query[0]}={(query[1])}&"

    return search_str


def _normalize_representations(record: dict, meta_data: dict):
    if "representations" in record:
        # Check if the record type is not "web_document" or "image"
        is_invalid_type = record["representations"]["record_type"] not in ["web_document", "image"]

        # Check if the meta_data indicates it's not downloadable
        is_not_downloadable = not meta_data["is_downloadable"]

        if is_invalid_type or is_not_downloadable:
            del record["representations"]

    return record


def _normalize_series(record: dict):
    """
    create a normalized series list with URL queries for each series

    "series": [
        {
            "label": "Personalsedler"
        },
        {
            "label": "V"
        }
    ],

    """

    if "series" in record and "collection" in record:
        """
        Add search_query to each series
        """
        series = record["series"]

        last_label = ""
        series_normalized = []
        for serie in series:
            label = last_label + serie["label"]
            last_label = label + "/"

            search_query = f"{_search_base_url}?collection={str(record['collection']['id'])}&series={label}"
            search_query = _normalize_search_query(search_query)
            serie["search_query"] = search_query
            series_normalized.append(serie)

        record["series"] = [series_normalized]

    if "series" in record and "collection" not in record:
        del record["series"]  # some series exist where there is no collection. Remove these as they are not searchable
    return record


def _normalize_content_types(record: dict):
    """
    Add search query to each content type
    """
    if "content_types" in record:
        content_types_list = record["content_types"]
        for content_type in content_types_list:
            for item in content_type:
                search_query = f"{_search_base_url}?content_types={str(item['id'])}"
                search_query = _normalize_search_query(search_query)
                item["search_query"] = search_query

        record["content_types"] = content_types_list
    return record


def _normalize_subjects(record: dict):
    """
    Add search query to each subject
    """
    if "subjects" in record:
        subjects = record["subjects"]
        for subject in subjects:
            for item in subject:
                search_query = f"{_search_base_url}?subjects={str(item['id'])}"
                search_query = _normalize_search_query(search_query)
                item["search_query"] = search_query

    return record


def _normalize_collection_tags(record: dict):
    """
    Add search query to each collection tag
    """

    collection_tags = []

    try:
        collection_id: int = record["collection"]["id"]
    except KeyError:
        return record

    if "collection_tags" in record:
        collection_tags = record["collection_tags"]

        for tag in collection_tags:
            query_str = str(urllib.parse.quote(tag["path"]))
            search_query = f"{_search_base_url}?collection={str(collection_id)}&collection_tags={query_str}"
            search_query = _normalize_search_query(search_query)
            tag["search_query"] = search_query

        record["collection_tags"] = collection_tags

    return record


def _normalize_dict_data(record: dict):
    """
    Transform dict value data to list of dict data. Then there is only one data structure to handle
    """
    if "admin_data" in record:
        record["admin_data"] = [record["admin_data"]]

    if "desc_data" in record:
        record["desc_data"] = [record["desc_data"]]
    return record


def _normalize_labels(record: dict):
    if "desc_data" in record and "source" in record["desc_data"]:
        record["desc_data"]["Kilde"] = record["desc_data"]["source"]
        del record["desc_data"]["source"]

    return record


def _normalize_resources(record: dict):
    """Transform resources to a more sane data structure: Same as content_types"""
    if "resources" in record:
        resources = record["resources"]
        item_dict_list = []
        for item_dict in resources:
            # move type to type
            item_dict = dict(sorted(item_dict.items(), key=lambda item: item[0] != "type"))
            item_dict_list.append(item_dict)

        record["resources"] = item_dict_list
    return record


def _normalize_link_lists(keys, record: dict):
    """add search_query to each link_list given in keys list"""
    for key in keys:
        if key in record:
            for item in record[key]:
                search_query = f"{_search_base_url}?{key}={str(item['id'])}"
                item["search_query"] = _normalize_search_query(search_query)
    return record


def _normalize_link_dicts(keys, record: dict):
    """add search_query to each link_dict given in keys list"""
    for key in keys:
        if key in record:
            item = record[key]
            search_query = f"{_search_base_url}?{key}={str(item['id'])}"
            item["search_query"] = _normalize_search_query(search_query)
    return record


def _get_list_of_type(type: str):
    """get a list of a type, e.g. string from record_definitions"""
    type_list = []
    for key, item in record_definitions.items():  # type: ignore
        if item["type"] == type:
            type_list.append(key)

    return type_list
