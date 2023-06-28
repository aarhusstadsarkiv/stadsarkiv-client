from stadsarkiv_client.core.logging import get_log
from stadsarkiv_client.records.normalize_abstract_dates import normalize_abstract_dates
from stadsarkiv_client.records.normalize_copyright_status import normalize_copyright_status
from stadsarkiv_client.records.normalize_contractual_status import normalize_contractual_status
from stadsarkiv_client.records.normalize_legal_restrictions import normalize_legal_restrictions
from stadsarkiv_client.records.normalize_availability import normalize_availability
from stadsarkiv_client.records.normalize_ordering import normalize_ordering
from stadsarkiv_client.records import normalize_record
from stadsarkiv_client.core.dynamic_settings import settings
from starlette.requests import Request


log = get_log()


def _get_list_of_type(type: str):
    """get a list of a type, e.g. string from record_definitions"""
    record_definitions = settings["record_definitions"]
    type_list = []
    for key, item in record_definitions.items():  # type: ignore
        if item["type"] == type:
            type_list.append(key)

    return type_list


def record_alter(request: Request, record: dict):
    record = record.copy()

    record = normalize_record.normalize_dict_data(record)
    record = normalize_record.normalize_collection_tags(record)
    record = normalize_record.normalize_series(record)
    record = normalize_record.normalize_content_types(record)
    record = normalize_record.normalize_subjects(record)
    record = normalize_record.normalize_labels(record)
    record = normalize_record.normalize_resources(record)

    link_list = _get_list_of_type("link_list")
    record = normalize_record.normalize_link_lists(link_list, record)

    link_dict = _get_list_of_type("link_dict")
    record = normalize_record.normalize_link_dicts(link_dict, record)

    record = normalize_abstract_dates(record)
    record = normalize_copyright_status(record)
    record = normalize_contractual_status(record)
    record = normalize_legal_restrictions(record)
    record = normalize_availability(record)
    record = normalize_ordering(record)

    return record


def get_section_data(sections, data):
    section_data = {}

    for section, keys in sections.items():
        section_values = {}
        for key in keys:
            if key in data:
                section_values[key] = data[key]

        if section_values:
            section_data[section] = section_values

    return section_data


def get_record_and_types(record):
    record_altered = {}
    for key, value in record.items():
        record_item = {}
        record_item["value"] = value
        record_item["name"] = key

        try:
            definition = settings["record_definitions"][key]
            record_item["type"] = definition["type"]
        except KeyError:
            record_item["type"] = "unknown"

        record_altered[key] = record_item

    return record_altered
