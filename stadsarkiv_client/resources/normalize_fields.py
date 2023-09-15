"""
File contains functions for normalizing fields in resources,
e.g. linkify strings, set outer years, etc.
"""

from stadsarkiv_client.core.logging import get_log
from stadsarkiv_client.core.translate import translate
from stadsarkiv_client.resources.resource_definitions import resource_definitions
import re
from urllib.parse import unquote


log = get_log()


def get_string_or_link_list(name: str, values: list):
    """
    Get string list and convert to link list if string contains ';'
    """
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


def set_sources_normalized(data: dict):
    """
    Set 'sources_normalized' field on dict
    """
    if "sources" in data:
        data["sources_normalized"] = _get_sources_normalized(data["sources"])

    return data


def set_outer_years(data: dict):
    """
    Set 'outer_years' field on dict
    """
    if "date_from" and "date_to" in data:
        outer_years = data["date_from"] + "-" + data["date_to"]
        data["outer_years"] = outer_years
    elif "date_from" in data:
        data["outer_years"] = data["date_from"]
    return data


def set_latitude_longitude(data: dict):
    """
    Set 'latitude_longitude_normalized' field on dict
    """
    if "latitude" and "longitude" in data:
        data["latitude_longitude"] = {
            "type": "string",
            "value": str(data["latitude"]) + ", " + str(data["longitude"]),
            "name": "latitude_longitude_normalized",
        }

    return data


def set_creators_link_list(data: dict):
    """
    Set creator_link field on dict.
    """

    if "is_creator" in data and data["is_creator"]:
        value = [
            {
                "search_query": f"creators={data['id_real']}",
                "label": translate("See all records this creator has created"),
            }
        ]
        data["creators_link"] = value

    return data


def set_collectors_link_list(data: dict):
    """
    Set collectors_link field on dict."""

    if "is_creator" in data and data["is_creative_creator"]:
        value = [
            {
                "search_query": f"collectors={data['id_real']}",
                "label": translate("See all records this organization has collected"),
            }
        ]
        data["collectors_link"] = value

    return data


def get_resource_and_types(resource):
    """
    Get resource with types
    """
    record_altered = {}
    for key, value in resource.items():
        resource_item = {}
        resource_item["value"] = value
        resource_item["name"] = key

        try:
            definition = resource_definitions[key]
            resource_item["type"] = definition["type"]
            record_altered[key] = resource_item
        except KeyError:
            # Don't alter if not defined
            record_altered[key] = value

    return record_altered


def _get_sources_normalized(sources: list):
    """
    Generate sources_normalized for sources
    """
    sources_normalized = []
    for i in range(len(sources)):
        sources_normalized.append(_linkify_str(sources[i]))

    return sources_normalized


def _should_linkify(value: str):
    """
    Check if string should be linkified. '1;collection'
    Split into id and label. If ';' in string, return True
    """
    value = value.strip()
    if value.find(";") != -1:
        return True

    return False


def _get_link_list(name: str, values: list):
    links = []
    for elem in values:
        id_label = elem.split(";")
        links.append({"search_query": f"{name}={id_label[0]}", "label": f"{id_label[1]}"})

    return links


def _linkify_str(text):
    pattern = r"(https?://\S+)"

    def replace_with_link(match):
        url = match.group(1)
        decoded_url = unquote(url)
        return f'<a href="{url}">{decoded_url}</a>'

    return re.sub(pattern, replace_with_link, text)
