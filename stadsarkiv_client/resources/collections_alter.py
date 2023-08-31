from stadsarkiv_client.core.logging import get_log
from stadsarkiv_client.resources import normalize_fields


log = get_log()


def collections_alter(collection: dict):
    collection = normalize_fields.set_sources_normalized(collection)
    collection = normalize_fields.set_outer_years(collection)
    collection = normalize_fields.get_resource_and_types(collection)

    # These are either string_list or link_list.
    string_list_or_link_list = [
        "collectors",
        "curators",
    ]

    for elem in string_list_or_link_list:
        if elem in collection:
            collection[elem] = normalize_fields.get_string_or_link_list(elem, collection[elem])

    return collection
