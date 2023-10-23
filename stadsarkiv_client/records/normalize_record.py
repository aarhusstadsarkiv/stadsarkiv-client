"""
Normalize record data from the API to a more sane data structure
"""

from stadsarkiv_client.core.logging import get_log
import urllib.parse
from stadsarkiv_client.records.record_definitions import record_definitions


log = get_log()


def normalize_record_data(record: dict, meta_data: dict):
    """
    Normalize record data to a more sane data structure
    """
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
    record = normalize_representations(record, meta_data)

    return record


def normalize_representations(record: dict, meta_data: dict):
    if "representations" in record:
        # if "record_type" is not "web_document" or "image" then remove it.
        if record["representations"]["record_type"] not in ["web_document", "image"]:
            del record["representations"]

        if not meta_data["is_downloadable"]:
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

            serie["search_query"] = "collection=" + str(record["collection"]["id"]) + "&series=" + urllib.parse.quote(label)

            series_normalized.append(serie)

        record["series"] = [series_normalized]
    else:
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
                item["search_query"] = "content_types=" + str(item["id"])

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
                item["search_query"] = "subjects=" + str(item["id"])

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
            tag["search_query"] = "collection=" + str(collection_id) + "&collection_tags=" + query_str

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
                item["search_query"] = key + "=" + str(item["id"])
    return record


def _normalize_link_dicts(keys, record: dict):
    """add search_query to each link_dict given in keys list"""
    for key in keys:
        if key in record:
            item = record[key]
            item["search_query"] = key + "=" + str(item["id"])
    return record


def _get_list_of_type(type: str):
    """get a list of a type, e.g. string from record_definitions"""
    type_list = []
    for key, item in record_definitions.items():  # type: ignore
        if item["type"] == type:
            type_list.append(key)

    return type_list
