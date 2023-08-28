from stadsarkiv_client.core.logging import get_log
import re
from urllib.parse import unquote


log = get_log()


def _should_linkify(value: str):
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


def get_string_or_link_list(name: str, values: list):
    """Get string list and convert to link list if needed if string contains ';'"""
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


def get_sources_normalized(data: list):
    # iterate data and linkify
    for i in range(len(data)):
        data[i] = _linkify_str(data[i])

    return {
        "type": "string_list",
        "value": data,
        "name": "sources",
    }


def set_outer_years(data: dict):
    """Set outer_years field on dict"""
    if "date_from" and "date_to" in data:
        outer_years = data["date_from"] + "-" + data["date_to"]
        data["outer_years"] = {
            "type": "string",
            "value": outer_years,
            "name": "outer_years",
        }
    elif "date_from" in data:
        data["outer_years"] = {
            "type": "string",
            "value": data["date_from"],
            "name": "outer_years",
        }
    return data
