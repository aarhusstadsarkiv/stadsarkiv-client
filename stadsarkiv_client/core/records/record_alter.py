from ..logging import get_log
from .normalize_abstract_dates import normalize_abstract_dates
from .normalize_copyright_status import normalize_copyright_status
from .normalize_contractual_status import normalize_contractual_status
from .normalize_legal_restrictions import normalize_legal_restrictions
from .normalize_availability import normalize_availability
from .normalize_ordering import normalize_ordering
from ..translate import translate
import urllib.parse
from starlette.requests import Request


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


def _is_allowed_by_ip(request: Request) -> bool:
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


def _normalize_series(record: dict):
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
            entry = {"collection": collection_id, "series": series, "search_url": "/search?" + query}
            series_normalized.append(entry)

        record["series_normalized"] = series_normalized
    return record


def _normalize_content_types(record: dict):
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
    tag_dict: dict = {}
    parts = tag.split("/")
    tag_dict["id"] = collection_id

    query_str = str(urllib.parse.quote(tag))
    tag_dict["query"] = query_str
    tag_dict["label"] = parts[-1]
    tag_dict["level"] = len(parts)
    tag_dict["search_url"] = f"/search?collection={collection_id}&collection_tags={query_str}"

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


def _is_sejrs_sedler(record_dict: dict):
    if "collection" not in record_dict:
        return False

    if record_dict["collection"].get("id") == 1:
        return True

    return False


def _set_representation_variables(record: dict):
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


def _set_common_variables(record: dict):
    record = _set_icon(record)

    # Set other keys in record dict
    record["copyright_id"] = record["copyright_status"].get("id")
    record["legal_id"] = record["other_legal_restrictions"].get("id")
    record["contractual_id"] = record["contractual_status"].get("id")
    record["availability_id"] = record["availability"].get("id")
    record["usability_id"] = record["usability"].get("id")

    return record


def record_alter(request: Request, record: dict):
    """Alter subjects, content_types and series to a more sane data structure"""

    record = record.copy()

    record["allowed_by_ip"] = _is_allowed_by_ip(request)
    record = _set_record_title(record)
    record = _set_common_variables(record)
    record = _set_representation_variables(record)

    record = _normalize_collection_tags(record)
    record = _normalize_series(record)
    record = _normalize_content_types(record)
    record = _normalize_subjects(record)

    record = normalize_abstract_dates(record)
    record = normalize_copyright_status(record)
    record = normalize_contractual_status(record)
    record = normalize_legal_restrictions(record)
    record = normalize_availability(record)
    record = normalize_ordering(record)

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
    copyright = ["copyright_status_normalized"]
    description_data = ["desc_data"]
    relations = ["organisations", "locations", "events", "people", "objects"]
    judicial_right_notes = ["rights_notes"]
    judicial_status = ["contractual_status_normalized", "other_legal_restrictions_normalized"]
    availability = ["availability_normalized"]
    ordering = ["ordering"]
    media = ["representations"]
    administration = ["admin_notes", "admin_data", "registration_id", "created_by", "created", "last_updated_by", "last_updated", "resources"]

    sections: dict = {
        "abstract": {},
        "description": {},
        "copyright": {},
        "description_data": {},
        "relations": {},
        "judicial_status": {},
        "judicial_right_notes": {},
        "availability": {},
        "ordering": {},
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
        elif key in description_data:
            sections["description_data"][key] = value
        elif key in relations:
            sections["relations"][key] = value
        elif key in judicial_right_notes:
            sections["judicial_right_notes"][key] = value
        elif key in judicial_status:
            sections["judicial_status"][key] = value
        elif key in availability:
            sections["availability"][key] = value
        elif key in ordering:
            sections["ordering"][key] = value
        elif key in media:
            sections["download"][key] = value

    sections["abstract"] = _sort_section(sections["abstract"], abstract)
    sections["description"] = _sort_section(sections["description"], description)
    sections["copyright"] = _sort_section(sections["copyright"], copyright)
    sections["description_data"] = _sort_section(sections["description_data"], description_data)
    sections["relations"] = _sort_section(sections["relations"], relations)
    sections["judicial_right_notes"] = _sort_section(sections["judicial_right_notes"], judicial_right_notes)
    sections["judicial_status"] = _sort_section(sections["judicial_status"], judicial_status)
    sections["availability"] = _sort_section(sections["availability"], availability)
    sections["ordering"] = _sort_section(sections["ordering"], ordering)
    sections["download"] = _sort_section(sections["download"], media)

    # check if record_dict does not contain one of the keys ['locations', 'people', 'events', 'organisations', 'objects']
    # if not, remove relations section
    if not any(key in record_dict for key in ["locations", "people", "events", "organisations", "objects"]):
        del sections["relations"]

    # check if section judicial_right_notes is empty
    # if so, remove judicial_right_notes section
    if not sections["judicial_right_notes"]:
        del sections["judicial_right_notes"]

    if not sections["description_data"]:
        del sections["description_data"]

    if not sections["ordering"]:
        del sections["ordering"]

    return sections


def _set_record_title(record_dict: dict):
    title = translate("No title")
    try:
        title = record_dict["heading"]
    except KeyError:
        pass

    record_dict["title"] = title
    return record_dict


__ALL__ = [get_sections, record_alter]
