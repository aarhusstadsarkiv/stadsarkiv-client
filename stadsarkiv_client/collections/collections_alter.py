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
        "type": "paragraphs",
        "value": value,
        "name": name,
    }


def _str_is_link(value: str):
    if value.find("http") != -1:
        return True

    return False


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
        "extent",
        "bulk_years",
        "accumulation_range",
    ]

    for elem in type_str:
        if elem in collection:
            collection[elem] = _str_to_type_str(elem, collection[elem])

    if "sources" in collection:
        if _str_is_link(collection["sources"][0]):
            sources = {
                "type": "link_list_external",
                "value": collection["sources"],
                "name": "sources",
            }
        else:
            sources = {
                "type": "string_list",
                "value": collection["sources"],
                "name": "sources",
            }

        collection["sources"] = sources

    if "collectors" in collection:
        links = _split_to_links("collectors", collection["collectors"])
        collection["collectors"] = links

    if "curators" in collection:
        links = _split_to_links("curators", collection["curators"])
        collection["curators"] = links

    # Add Yderår: outer_years
    if "date_from" and "date_to" in collection:
        outer_years = collection["date_from"] + "-" + collection["date_to"]
        collection["outer_years"] = {
            "type": "string",
            "value": outer_years,
            "name": "outer_years",
        }

    return collection
