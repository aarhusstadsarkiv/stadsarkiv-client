from stadsarkiv_client.core.logging import get_log
import urllib.parse
from starlette.requests import Request
from stadsarkiv_client.core.translate import translate


log = get_log()


IP_ALLOW = ["193.33.148.24"]


ICONS = {
    "61": {"icon": "image", "label": "Billeder"},
    "95": {"icon": "laptop_mac", "label": "Elektronisk materiale"},
    "10": {"icon": "gavel", "label": "Forskrifter og vedtægter"},
    "1": {"icon": "folder_open", "label": "Kommunale sager og planer"},
    "75": {"icon": "map", "label": "Kortmateriale"},
    "49": {"icon": "description", "label": "Manuskripter"},
    "87": {"icon": "movie", "label": "Medieproduktioner"},
    "81": {"icon": "audio_file", "label": "Musik og lydoptagelser"},
    "36": {"icon": "menu_book", "label": "Publikationer"},
    "18": {"icon": "local_library", "label": "Registre og protokoller"},
    "29": {"icon": "bar_chart", "label": "Statistisk og økonomisk materiale"},
    "99": {"icon": "description", "label": "Andet materiale"},
}


def is_allowed_by_ip(request: Request) -> bool:
    ip = request["client"][0]
    if ip in IP_ALLOW:
        return True
    return False


def _list_dict_id_label(original_data):
    """Transform to a more sane data structure:
    original_data = [{"id": [1, 2, 3], "label": ["a", "b", "c"]}]
    transformed_data = [{"id": 1, "label": "a"}, {"id": 2, "label": "b"}, {"id": 3, "label": "c"}]"""
    transformed_data = [
        {"id": item["id"][index], "label": item["label"][index]} for item in original_data for index in range(len(item["id"]))
    ]
    return transformed_data


def normalize_series(record: dict):
    """create a normalized series list with URL query for each series"""

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
    return record


def normalize_content_types(record: dict):
    """Transform content_types to a more sane data structure ( list of list of dicts)
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


def normalize_subjects(record: dict):
    """Transform subjects to a more sane data structure: Same as content_types"""
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
    tag_dict: dict = {}
    parts = tag.split("/")
    tag_dict["id"] = collection_id

    query_str = str(urllib.parse.quote(tag))
    tag_dict["query"] = query_str
    tag_dict["label"] = parts[-1]
    tag_dict["level"] = len(parts)
    tag_dict["search_query"] = f"collection={collection_id}&collection_tags={query_str}"

    return tag_dict


def normalize_hierarchy(collection_id: int, tags_list: list):
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


def normalize_collection_tags(record: dict):
    # For future testing
    # log.debug(_normalize_hierarchy(1, ["a", "a/b", "c", "c/d", "c/d/e"]))

    collection_tags = []

    try:
        collection_id: int = record["collection"]["id"]
    except KeyError:
        return record

    if "collection_tags" in record:
        collection_tags = normalize_hierarchy(collection_id, record["collection_tags"])
        record["collection_tags"] = collection_tags

    return record


def normalize_dict_data(record: dict):
    """Transform dict value data to list of dict data. Then there is only one data structure to handle"""
    if "admin_data" in record:
        record["admin_data"] = [record["admin_data"]]

    if "desc_data" in record:
        record["desc_data"] = [record["desc_data"]]
    return record


def normalize_labels(record: dict):
    if "desc_data" in record and "source" in record["desc_data"]:
        record["desc_data"]["Kilde"] = record["desc_data"]["source"]
        del record["desc_data"]["source"]

    return record


def normalize_resources(record: dict):
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


def normalize_link_lists(keys, record: dict):
    """add search_query to each link_list given in keys list"""
    for key in keys:
        if key in record:
            for item in record[key]:
                item["search_query"] = key + "=" + str(item["id"])
    return record


def normalize_link_dicts(keys, record: dict):
    """add search_query to each link_dict given in keys list"""
    for key in keys:
        if key in record:
            item = record[key]
            item["search_query"] = key + "=" + str(item["id"])
    return record


def _set_icon(record: dict):
    """Set icon for the record based on content type"""
    try:
        content_type_id = record["content_types"][0][0]["id"]
        record["icon"] = ICONS[str(content_type_id)]
    except KeyError:
        record["icon"] = ICONS["99"]

    return record


def _is_sejrs_sedler(record_dict: dict):
    if "collection" not in record_dict:
        return False

    if record_dict["collection"].get("id") == 1:
        return True

    return False


def set_representation_variables(record: dict):
    # Set record_type if record.representations exists
    record["record_type"] = None
    if "representations" in record:
        record["record_type"] = record["representations"].get("record_type")

    record["has_representations"] = False
    if record["legal_id"] == 1 and record["contractual_id"] > 2:
        # Then it is a representation, image, audio, video, web_document - or notice about reading room
        record["has_representations"] = True

    record["is_representations_online"] = False
    if record["availability_id"] == 4 or record["allowed_by_ip"]:
        record["is_representations_online"] = True

    if _is_sejrs_sedler(record):
        record["record_type"] = "sejrs_sedler"

    return record


def set_download_variables(record: dict) -> dict:
    record["is_downloadable"] = (
        record.get("representations")
        and record["legal_id"] == 1
        and record["contractual_id"] > 3
        and record["usability_id"] in [1, 2, 3]
        and record["record_type"] != "video"
    )
    return record


def set_common_variables(record: dict):
    record = _set_icon(record)

    # Set other keys in record dict
    record["copyright_id"] = record["copyright_status"].get("id")
    record["legal_id"] = record["other_legal_restrictions"].get("id")
    record["contractual_id"] = record["contractual_status"].get("id")
    record["availability_id"] = record["availability"].get("id")
    record["usability_id"] = record["usability"].get("id")

    return record


def set_record_title(record_dict: dict):
    title = translate("No title")
    record_title = record_dict.get("title")
    if not record_title:
        record_title = record_dict.get("heading")

    if record_title:
        title = record_title

    record_dict["title"] = title
    return record_dict
