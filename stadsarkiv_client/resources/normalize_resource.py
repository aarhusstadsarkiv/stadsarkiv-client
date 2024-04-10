"""
File contains functions for normalizing fields in resources,
e.g. linkify strings, set outer years, etc.
"""

from stadsarkiv_client.core.logging import get_log
from stadsarkiv_client.resources.resource_definitions import resource_definitions
from stadsarkiv_client.core.translate import translate
import re
from urllib.parse import unquote
from stadsarkiv_client.core.dynamic_settings import settings


_search_base_url = settings["search_base_url"]


log = get_log()


def get_string_or_link_list(name: str, values: list):
    """
    Get string list and convert to link list if string contains ';'
    """
    should_linkify = _should_linkify(values[0])
    if should_linkify:
        links = _get_link_list(name, values)
        return links
    else:
        return values


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
    if "date_from" in data and "date_to" in data:
        outer_years = data["date_from"] + "-" + data["date_to"]
        data["outer_years"] = outer_years
    elif "date_from" in data:
        data["outer_years"] = data["date_from"]
    return data


def set_created_decommissioned(data: dict):
    """
    copy date_from to date_created and date_to to date_decommissioned
    """
    if "date_from" in data:
        data["date_created"] = data["date_from"]

    if "date_to" in data:
        data["date_decommissioned"] = data["date_to"]

    return data


def set_latitude_longitude(data: dict):
    """
    Set 'latitude_longitude_normalized' field on dict
    """
    if "latitude" and "longitude" in data:
        data["latitude_longitude_normalized"] = {
            "latitude": str(data["latitude"]),
            "longitude": str(data["longitude"]),
        }

    return data


def set_creators_link_list(data: dict, schema):
    """
    Set creator_link field on dict.
    """
    is_creator = data.get("is_creator", False)
    is_creative_creator = data.get("is_creative_creator", False)

    if is_creator and is_creative_creator:
        label_key = "creator" if schema == "person" else "organization"
        label = translate(f"See all records this {label_key} has created")

        data["creators_link"] = [
            {
                "search_query": f"{_search_base_url}?creators={data['id_real']}",
                "label": label,
            }
        ]

    return data


def set_collectors_link_list(data: dict, schema):
    """
    Set collectors_link field on dict.
    """
    is_creator = data.get("is_creator", False)

    if is_creator:
        label_key = "creator" if schema == "person" else "organization"
        label = translate(f"See all records this {label_key} has collected")

        data["collectors_link"] = [
            {
                "search_query": f"{_search_base_url}?collectors={data['id_real']}",
                "label": label,
            }
        ]

    return data


def set_persons_link_list(data: dict, schema):
    """
    Set person_link field on dict.
    """
    if schema == "person":
        data["persons_links"] = [
            {
                "search_query": f"{_search_base_url}?people={data['id_real']}",
                "label": translate("See all records about this person"),
            },
            {
                "search_query": f"{_search_base_url}?creators={data['id_real']}",
                "label": translate("See all records this person has created"),
            },
        ]

    return data


def alter_portrait_hightlights(resource: dict):
    if "portrait" in resource:
        resource["portrait"] = [_http_to_https(val) for val in resource["portrait"]]

    if "highlights" in resource:
        resource["highlights"] = [_http_to_https(val) for val in resource["highlights"]]

    return resource


def get_resource_and_types(resource):
    """
    Get resource with types
    """
    resource_altered = {}
    resource_altered["meta"] = {}
    for key, value in resource.items():
        resource_item = {}
        resource_item["value"] = value
        resource_item["name"] = key

        try:
            definition = resource_definitions[key]
            resource_item["type"] = definition["type"]
            resource_item["label"] = translate("label_" + key)
            resource_altered[key] = resource_item

        except KeyError:
            # create meta dict
            if key in ["id_real", "schema"]:
                resource_altered["meta"][key] = value

    return resource_altered


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
        links.append({"search_query": f"{_search_base_url}?{name}={id_label[0]}", "label": f"{id_label[1]}"})

    return links


def _http_to_https(url: str):
    if url.startswith("http://"):
        url = url.replace("http://", "https://")

    return url


def _linkify_str(text):
    pattern = r"(https?://\S+)"

    def replace_with_link(match):
        url = match.group(1)

        url = _http_to_https(url)

        decoded_url = unquote(url)
        return f'<a href="{url}">{decoded_url}</a>'

    return re.sub(pattern, replace_with_link, text)
