from stadsarkiv_client.core.logging import get_log
from stadsarkiv_client.resources import normalize_fields


log = get_log()

type_str = [
    "date_from",
    "date_to",
    "description",
    "display_label",
    "domain",
    "local_area",
]

lists = [
    "industry",
]


def creators_alter(creator: dict):
    # creator = normalize_fields.set_latitude_longitude(creator)
    creator = normalize_fields.set_creators_link_list(creator)
    creator = normalize_fields.set_collectors_link_list(creator)
    for elem in type_str:
        if elem in creator:
            creator[elem] = normalize_fields.str_to_type_str(elem, creator[elem])

    for elem in lists:
        if elem in creator:
            creator[elem] = normalize_fields.list_to_type_list(elem, creator[elem])

    if "sources" in creator:
        creator["sources"] = normalize_fields.get_sources_normalized(creator["sources"])

    return creator
