from stadsarkiv_client.core.logging import get_log
from stadsarkiv_client.resources import normalize_fields


log = get_log()

type_str = [
    "summary",
    "description",
    "content_and_scope",
    "access",
    "legal_status",
    "level_of_digitisation",
    "citation",
    "custodial_history",
    "level_of_kassation",
    "accrual_status",
    "system_of_arrangement",
    "archival_history",
    "extent",
    "bulk_years",
    "accumulation_range",
]

string_link_list = [
    "collectors",
    "curators",
]


def _str_to_type_str(name: str, value: str):
    return {
        "type": "paragraphs",
        "value": value,
        "name": name,
    }


def collections_alter(collection: dict):
    for elem in type_str:
        if elem in collection:
            collection[elem] = _str_to_type_str(elem, collection[elem])

    for elem in string_link_list:
        if elem in collection:
            collection[elem] = normalize_fields.get_string_or_link_list(elem, collection[elem])

    collection = normalize_fields.set_outer_years(collection)
    if "sources" in collection:
        collection["sources"] = normalize_fields.get_sources_normalized(collection["sources"])

    return collection
