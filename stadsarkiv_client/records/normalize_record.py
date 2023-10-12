"""
Normalize record data from the API to a more sane data structure
"""

from stadsarkiv_client.core.logging import get_log
import urllib.parse
from stadsarkiv_client.records.record_definitions import record_definitions


log = get_log()


def normalize_record_data(record: dict):
    """
    Normalize record data to a more sane data structure
    """
    record = _normalize_dict_data(record)
    record = _normalize_collection_tags(record)
    record = _normalize_series(record)
    record = _normalize_content_types(record)
    record = _normalize_subjects(record)
    record = _normalize_labels(record)
    record = _normalize_resources(record)

    link_list = _get_list_of_type("link_list")
    record = _normalize_link_lists(link_list, record)

    link_dict = _get_list_of_type("link_dict")
    record = _normalize_link_dicts(link_dict, record)

    record = normalize_representations(record)

    return record


def normalize_representations(record: dict):
    if "representations" in record:
        # if "record_type" is not "web_document" or "image" then remove it.
        if record["representations"]["record_type"] not in ["web_document", "image"]:
            del record["representations"]

    return record


def _list_dict_id_label(original_data):
    """
    Transform to a more sane data structure:
    original_data = [{"id": [1, 2, 3], "label": ["a", "b", "c"]}]
    transformed_data = [{"id": 1, "label": "a"}, {"id": 2, "label": "b"}, {"id": 3, "label": "c"}]"""
    transformed_data = [
        {"id": item["id"][index], "label": item["label"][index]} for item in original_data for index in range(len(item["id"]))
    ]
    return transformed_data


def _normalize_series(record: dict):
    """
    create a normalized series list with URL queries for each series
    """

    if "series" in record and "collection" in record:
        series_normalized = []
        series_list = record["series"].split("/")
        collection_id = record["collection"]["id"]

        query = "collection=" + str(collection_id) + "&series="
        for series in series_list:
            # if not first part of the url query then add '/' to query
            if series != series_list[0]:
                query += urllib.parse.quote("/")

            query += urllib.parse.quote(series)
            entry = {"collection": collection_id, "label": series, "search_query": query}
            series_normalized.append(entry)

        record["series"] = [series_normalized]

    if "collection" not in record:
        # Remove series from record if it does not have a collection
        # This should not happen, but it does. Should be fixed in the API
        if "series" in record:
            del record["series"]
    return record


def _normalize_content_types(record: dict):
    """
    Transform content_types to a more sane data structure ( list of list of dicts)
    original_data = [
            {'id': [61, 102], 'label': ['Billeder', 'Situations billeder']},
            {'id': [61, 68], 'label': ['Billeder', 'Maleri']}
        ]
    transformed_data = [
        [{'id': 61, 'label': 'Billeder'}, {'id': 102, 'label': 'Situations billeder'}],
        [{'id': 61, 'label': 'Billeder'}, {'id': 68, 'label': 'Maleri'}]
    ]
    """

    if "content_types" in record:
        content_types = record["content_types"]
        content_types_list = []
        for content_type in content_types:
            content_types_list.append(_list_dict_id_label([content_type]))

        """ add search query to each content type """
        for content_type in content_types_list:
            for item in content_type:
                item["search_query"] = "content_types=" + str(item["id"])

        record["content_types"] = content_types_list
    return record


def _normalize_subjects(record: dict):
    """
    Transform subjects to a more sane data structure: Same as content_types
    """
    if "subjects" in record:
        subjects = record["subjects"]
        subjects_list = []
        for content_type in subjects:
            subjects_list.append(_list_dict_id_label([content_type]))

        """ add search query to each subject """
        for subject in subjects_list:
            for item in subject:
                item["search_query"] = "subjects=" + str(item["id"])
        record["subjects"] = subjects_list
    return record


def _get_collection_tag(collection_id: int, tag: str):
    """
    Get data for a collection tag
    """
    tag_dict: dict = {}
    parts = tag.split("/")
    tag_dict["id"] = collection_id

    query_str = str(urllib.parse.quote(tag))
    tag_dict["query"] = query_str
    tag_dict["label"] = parts[-1]
    tag_dict["level"] = len(parts)
    tag_dict["search_query"] = f"collection={collection_id}&collection_tags={query_str}"

    return tag_dict


def _normalize_hierarchy(collection_id: int, tags_list: list):
    """
    Transform a list of tags to a list of lists of tags
    """
    result = []
    current_level = 1
    current_list: list = []

    for tag in tags_list:
        tag_dict = _get_collection_tag(collection_id, tag)

        if tag_dict["level"] == 1:
            # Append the current list to the result
            # Starting a new list for a new hierarchy level
            if current_list:
                result.append(current_list)
            current_list = [tag_dict]
        elif tag_dict["level"] == current_level + 1:
            # Add a tag to the current list
            current_list.append(tag_dict)
        else:
            raise ValueError("Invalid tag hierarchy")

        current_level = tag_dict["level"]

    if current_list:
        result.append(current_list)

    return result


def _normalize_collection_tags(record: dict):
    """
    noramlize collection tags

    """
    # log.debug(_normalize_hierarchy(1, ["a", "a/b", "c", "c/d", "c/d/e"]))

    collection_tags = []

    try:
        collection_id: int = record["collection"]["id"]
    except KeyError:
        return record

    if "collection_tags" in record:
        collection_tags = _normalize_hierarchy(collection_id, record["collection_tags"])
        record["collection_tags"] = collection_tags

    return record


def _normalize_dict_data(record: dict):
    """Transform dict value data to list of dict data. Then there is only one data structure to handle"""
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
    # record_definitions = settings["record_definitions"]
    type_list = []
    for key, item in record_definitions.items():  # type: ignore
        if item["type"] == type:
            type_list.append(key)

    return type_list
