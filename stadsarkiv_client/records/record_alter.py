from stadsarkiv_client.core.logging import get_log
from .normalize_abstract_dates import normalize_abstract_dates
from .normalize_copyright_status import normalize_copyright_status
from .normalize_contractual_status import normalize_contractual_status
from .normalize_legal_restrictions import normalize_legal_restrictions
from .normalize_availability import normalize_availability
from .normalize_ordering import normalize_ordering
from stadsarkiv_client.core.translate import translate
from .import normalize_record
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


def record_alter(request: Request, record: dict):
    """Alter subjects, content_types and series to a more sane data structure"""

    record = record.copy()

    record["allowed_by_ip"] = normalize_record.is_allowed_by_ip(request)
    record = normalize_record.set_record_title(record)
    record = normalize_record.set_common_variables(record)
    record = normalize_record.set_representation_variables(record)

    record = normalize_record.set_download_variables(record)
    record = normalize_record.normalize_collection_tags(record)
    record = normalize_record.normalize_series(record)
    record = normalize_record.normalize_content_types(record)
    record = normalize_record.normalize_subjects(record)
    record = normalize_record.normalize_labels(record)
    record = normalize_record.normalize_resources(record)

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
    administration = [
        "admin_notes",
        "admin_data",
        "registration_id",
        "created_by",
        "created",
        "last_updated_by",
        "last_updated",
    ]

    resources = ["resources"]
    download = ["representations"]

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
        "administration": {},
        "resources": {},
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
        elif key in administration:
            sections["administration"][key] = value
        elif key in resources:
            sections["resources"][key] = value
        elif key in download:
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
    sections["administration"] = _sort_section(sections["administration"], administration)
    sections["resources"] = _sort_section(sections["resources"], resources)
    sections["download"] = _sort_section(sections["download"], download)

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

    if not sections["resources"]:
        del sections["resources"]

    if not record_dict["is_downloadable"]:
        del sections["download"]

    return sections
