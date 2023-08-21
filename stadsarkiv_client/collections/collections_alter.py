from stadsarkiv_client.core.logging import get_log

log = get_log()


def _should_linkify(value: str):
    if value.find(";") != -1:
        return True

    return False


def _get_link_list(name: str, values: list):
    links = []
    for elem in values:
        id_label = elem.split(";")
        links.append({"search_query": f"{name}={id_label[0]}", "label": f"{id_label[1]}"})

    return links


def _split_to_links(name: str, values: list):
    should_linkify = _should_linkify(values[0])
    if should_linkify:
        links = _get_link_list(name, values)

        return {
            "type": "link_list",
            "value": links,
            "name": name,
        }

    else:
        return {
            "type": "string_list",
            "value": values,
            "name": name,
        }


def _str_to_type_str(name: str, value: str):
    return {
        "type": "string",
        "value": value,
        "name": name,
    }


def collections_alter(collection: dict):
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
    ]

    for elem in type_str:
        if elem in collection:
            collection[elem + "_test"] = _str_to_type_str(elem, collection[elem])

    if "sources" in collection:
        links = _split_to_links("sources", collection["sources"])
        collection["sources_test"] = links
        log.debug(f"links: {links}")

    if "collectors" in collection:
        links = _split_to_links("collectors", collection["collectors"])
        log.debug(f"links: {links}")
        collection["collectors_test"] = links

    if "curators" in collection:
        links = _split_to_links("curators", collection["curators"])
        log.debug(f"links: {links}")
        collection["curators_test"] = links
        # collection['collectors'] = _split_to_links(collection['collectors'])

    return collection
