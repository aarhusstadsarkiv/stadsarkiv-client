from stadsarkiv_client.core.logging import get_log
import urllib.parse


log = get_log()


def _list_dict_id_label(original_data):
    """Transform to a more sane data structure:
    original_data = [{"id": [1, 2, 3], "label": ["a", "b", "c"]}]
    transformed_data = [{"id": 1, "label": "a"}, {"id": 2, "label": "b"}, {"id": 3, "label": "c"}]"""
    transformed_data = [
        {"id": item["id"][index], "label": item["label"][index]}
        for item in original_data
        for index in range(len(item["id"]))
    ]
    return transformed_data


def _normalize_series(record: dict):
    """create a normalized series list with URL query for each series"""

    if "series" in record and "collection" in record:
        series_normalized = []
        series_list = record["series"].split("/")
        collection_id = record["collection"]["id"]

        query = "collection=" + str(collection_id) + "&series="
        for series in series_list:
            # if not first or last in series add '/' to query
            if series != series_list[0] and series != series_list[-1]:
                query += urllib.parse.quote("/")

            query += urllib.parse.quote(series)
            entry = {"collection": collection_id, "series": series, "query": query}
            series_normalized.append(entry)

        record["series_normalized"] = series_normalized
    return record


def _normalize_content_types(record: dict):
    """Transform content_types to a more sane data structure:
    original_data = [{'id': [61, 102], 'label': ['Billeder', 'Situations billeder']}, {'id': [61, 68], 'label': ['Billeder', 'Maleri']}]
    transformed_data = [[{'id': 61, 'label': 'Billeder'}, {'id': 102, 'label': 'Situations billeder'}], [{'id': 61, 'label': 'Billeder'}, {'id': 68, 'label': 'Maleri'}]]
    """

    if "content_types" in record:
        content_types = record["content_types"]
        content_types_list = []
        for content_type in content_types:
            content_types_list.append(_list_dict_id_label([content_type]))
        record["content_types_normalized"] = content_types_list
    return record


def _normalize_subjects(record: dict):
    """Transform subjects to a more sane data structure: Same as content_types"""
    if "subjects" in record:
        subjects = record["subjects"]
        subjects_list = []
        for content_type in subjects:
            subjects_list.append(_list_dict_id_label([content_type]))
        record["subjects_normalized"] = subjects_list
    return record


def _normalize_abstract_dates(record: dict):
    if "date_from" in record and "date_to" in record:
        date_from = record["date_from"]
        date_to = record["date_to"]
        if date_from == date_to:
            record["date_normalized"] = date_from
        else:
            record["date_normalized"] = date_from + " ~ " + date_to

    return record


def _normalize_hierarchy(collection_id: int, list_tags: list):
    result = []
    current_level = 1
    current_list = []

    for tag in list_tags:
        tag_dict = {}
        parts = tag.split("/")
        tag_dict["id"] = collection_id
        tag_dict["query"] = urllib.parse.quote(tag)
        tag_dict["label"] = parts[-1]
        tag_dict["level"] = len(parts)

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

    log.debug(_normalize_hierarchy(1, ["a", "a/b", "c", "c/d", "c/d/e"]))

    collection_tags = []

    try:
        collection_id = record["collection"]["id"]
    except KeyError:
        return record

    if "collection_tags" in record:
        collection_tags = _normalize_hierarchy(collection_id, record["collection_tags"])

        # test = _normalize_hierarchy(collection_id, record["collection_tags"])
        # log.debug(test)
        record["collection_tags_normalized"] = collection_tags

    return record


def alter_record(record: dict):
    """Alter subjects, content_types and series to a more sane data structure"""

    record = _normalize_collection_tags(record)
    record = _normalize_abstract_dates(record)
    record = _normalize_series(record)
    record = _normalize_content_types(record)
    record = _normalize_subjects(record)

    return record


def _sort_section(section: dict, order: list):
    sorted_section = {key: section[key] for key in order if key in section}
    return sorted_section


def get_sections(record_dict: dict):
    abstract = ["collectors", "content_types_normalized", "creators", "date_normalized", "curators", "id"]
    description = [
        "heading",
        "summary",
        "desc_notes",
        "collection",
        "series_normalized",
        "collection_tags_normalized",
        "subjects_normalized",
    ]
    copyright = ["copyright_status"]
    relations = ["organisations", "locations", "events", "people"]
    copyright_extra = ["contractual_status", "other_legal_restrictions"]
    availability = ["availability"]
    media = ["representations"]

    sections: dict = {
        "abstract": {},
        "description": {},
        "copyright": {},
        "relations": {},
        "copyright_extra": {},
        "availability": {},
        "download": {},
        "other": {},
    }

    for key, value in record_dict.items():
        if key in abstract:
            sections["abstract"][key] = value
        elif key in description:
            sections["description"][key] = value
        elif key in copyright:
            sections["copyright"][key] = value
        elif key in relations:
            sections["relations"][key] = value
        elif key in copyright_extra:
            sections["copyright_extra"][key] = value
        elif key in availability:
            sections["availability"][key] = value
        elif key in media:
            sections["download"][key] = value

    sections["abstract"] = _sort_section(sections["abstract"], abstract)
    sections["description"] = _sort_section(sections["description"], description)
    sections["copyright"] = _sort_section(sections["copyright"], copyright)
    sections["relations"] = _sort_section(sections["relations"], relations)
    sections["copyright_extra"] = _sort_section(sections["copyright_extra"], copyright_extra)
    sections["availability"] = _sort_section(sections["availability"], availability)
    sections["download"] = _sort_section(sections["download"], media)

    return sections


def get_record_title(record_dict: dict):
    title = None
    try:
        title = record_dict["heading"]
    except KeyError:
        pass

    return title


def get_record_image(record_dict: dict):
    image = None
    try:
        if record_dict["representations"]["record_type"] == "image":
            image = record_dict["representations"]["record_image"]
    except KeyError:
        pass

    return image


def get_sejrs_sedler(record_dict: dict):
    if "collection" not in record_dict:
        return None

    if record_dict["collection"] == 1 or "summary" in record_dict:
        return record_dict["summary"]
