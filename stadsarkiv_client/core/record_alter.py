from .logging import get_log
from .record_date import normalize_abstract_dates
import urllib.parse
from starlette.requests import Request


log = get_log()


IP_WHITELIST = ["193.33.148.24"]


ICONS = {
    "61": {"icon": "far fa-image", "label": "Billeder"},
    "95": {"icon": "fas fa-laptop", "label": "Elektronisk materiale"},
    "10": {"icon": "fas fa-gavel", "label": "Forskrifter og vedtægter"},
    "1": {"icon": "far fa-folder-open", "label": "Kommunale sager og planer"},
    "75": {"icon": "far fa-map", "label": "Kortmateriale"},
    "49": {"icon": "far fa-file-alt", "label": "Manuskripter"},
    "87": {"icon": "fas fa-film", "label": "Medieproduktioner"},
    "81": {"icon": "fas fa-music", "label": "Musik og lydoptagelser"},
    "36": {"icon": "fas fa-book", "label": "Publikationer"},
    "18": {"icon": "fab fa-leanpub", "label": "Registre og protokoller"},
    "29": {"icon": "far fa-chart-bar", "label": "Statistisk og økonomisk materiale"},
    "99": {"icon": "far fa-file", "label": "Andet materiale"},
}


def _is_readingroom(request: Request) -> bool:
    ip = request['client'][0]
    if ip in IP_WHITELIST:
        return True
    return False


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
    """Transform content_types to a more sane data structure ( list of list of dicts)
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


def _get_collection_tag(collection_id: int, tag: str):
    tag_dict = {}
    parts = tag.split("/")
    tag_dict["id"] = collection_id

    query_str = str(urllib.parse.quote(tag))
    tag_dict["query"] = query_str
    tag_dict["label"] = parts[-1]
    tag_dict["level"] = len(parts)

    return tag_dict


def _normalize_hierarchy(collection_id: int, tags_list: list):
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
    # For future testing
    # log.debug(_normalize_hierarchy(1, ["a", "a/b", "c", "c/d", "c/d/e"]))

    collection_tags = []

    try:
        collection_id: int = record["collection"]["id"]
    except KeyError:
        return record

    if "collection_tags" in record:
        collection_tags = _normalize_hierarchy(collection_id, record["collection_tags"])
        record["collection_tags_normalized"] = collection_tags

    return record


def _set_icon(record: dict):
    """Set icon for the record based on content type"""
    try:
        content_type_id = record["content_types_normalized"][0][0]["id"]
        record["icon"] = ICONS[str(content_type_id)]
    except KeyError:
        record["icon"] = ICONS["99"]

    return record


def _set_representation_variables(record: dict):

    # Set record_type if record.representations exists
    record["record_type"] = None
    if 'representations' in record:
        record['record_type'] = record['representations'].get('record_type')

    record["has_representations"] = False
    if record['legal_id'] == 1 and record['contractual_id'] > 2:
        # Then it is a representation, image, audio, video or text
        record["has_representations"] = True

    record["is_representations_online"] = False
    if record["availability_id"] == 4 or record["readingroom"]:
        record["is_representations_online"] = True

    return record


def _set_common_variables(record: dict):

    record = _set_icon(record)

    # Set other keys in record dict
    record['copyright_id'] = record['copyright_status'].get('id')
    record['legal_id'] = record['other_legal_restrictions'].get('id')
    record['contractual_id'] = record['contractual_status'].get('id')
    record['availability_id'] = record['availability'].get('id')
    record['usability_id'] = record['usability'].get('id')

    return record


def record_alter(request: Request, record: dict):
    """Alter subjects, content_types and series to a more sane data structure"""

    record = _normalize_collection_tags(record)
    record = normalize_abstract_dates(record)
    record = _normalize_series(record)
    record = _normalize_content_types(record)
    record = _normalize_subjects(record)

    record['readingroom'] = _is_readingroom(request)
    record = _set_common_variables(record)
    record = _set_representation_variables(record)

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
