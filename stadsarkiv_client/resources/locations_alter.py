from stadsarkiv_client.core.logging import get_log
from stadsarkiv_client.resources import normalize_fields


log = get_log()

type_str = [
    "name",
    "addr_nr",
    "zipcode",
    "description",
    "display_label",
    "domain",
    "latitude",
    "longitude",
    "local_area",
    "parish",
    "rotation",
]

lists = [
    "alt_names",
]


def locations_alter(location: dict):
    location = normalize_fields.set_latitude_longitude(location)
    for elem in type_str:
        if elem in location:
            location[elem] = normalize_fields.str_to_type_str(elem, location[elem])

    if "sources" in location:
        location["sources"] = normalize_fields.get_sources_normalized(location["sources"])

    return location
