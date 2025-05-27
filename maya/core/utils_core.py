"""
Module for parsing and formatting structured JSON-like data records into various output formats
(HTML, plain text, or HTML tables), based on associated metadata types.

This module provides utility functions for transforming dictionaries of data with typed values
(e.g., links, strings, dates, etc.) into user-friendly display formats. It supports both
HTML-formatted output for web display and plain text versions for non-HTML contexts.

Functions:
- get_record_and_types_as_html(data, keys_to_parse, section_tag='p'):
    Parses specified keys from the input data and formats the values into an HTML structure
    using the provided section tag (e.g., 'p', 'div').

- get_record_and_types_as_strings(data, keys_to_parse):
    Converts the data values of specified keys into plain strings, removing any hyperlink formatting
    while preserving basic structure (e.g., hierarchies).

- get_parsed_data_as_str(data, keys_to_parse):
    Formats the parsed data as a single HTML string using <div> elements and translated field labels.

- get_parsed_data_as_table(data, keys_to_parse, debug=False):
    Returns an HTML table representing the parsed data with field labels and values.
    Optionally includes original key names if debug=True.

- get_parsed_data_as_html(data, keys_to_parse, section_tag='p'):
    Returns an HTML string with each key/value pair wrapped in a <div> tag. Values are
    formatted based on their type and wrapped in the specified section tag.

"""

from typing import Dict, List, Any
from maya.core.translate import translate


def get_record_and_types_as_html(data: Dict[str, Any], keys_to_parse: List[str], section_tag: str = "p") -> Dict[str, str]:
    """
    Parses specific keys in a JSON dictionary according a data-type and .
    """
    parsed_data = {}

    section_separator = f"<{section_tag}>" if section_tag else ""
    closing_tag = f"</{section_tag}>" if section_tag else ""

    for key in keys_to_parse:
        if key not in data:
            continue

        value = data[key]["value"]
        data_type = data[key]["type"]

        if value is None:
            parsed_data[key] = ""
            continue

        if data_type == "link_list":
            parsed_data[key] = (
                section_separator
                + (section_separator.join(f'<a href="{item["search_query"]}">{item["label"]}</a>' for item in value))
                + closing_tag
            )

        elif data_type == "link_dict":
            parsed_data[key] = f'<a href="{value["search_query"]}">{value["label"]}</a>'
        elif data_type == "link_list_hierarchy":

            parsed_hierarchy = []
            for sublist in value:
                hierarchy_links = " > ".join(f'<a href="{item["search_query"]}">{item["label"]}</a>' for item in sublist)
                parsed_hierarchy.append(hierarchy_links)
            parsed_data[key] = section_separator + section_separator.join(parsed_hierarchy) + closing_tag

        elif data_type == "label_dict":
            parsed_data[key] = value["label"] if isinstance(value, dict) else ""
        elif data_type == "string":
            parsed_data[key] = str(value)
        elif data_type == "date":
            parsed_data[key] = str(value)
        elif data_type == "string_list":
            parsed_data[key] = section_separator + section_separator.join(value) + closing_tag if isinstance(value, list) else ""

        elif data_type == "key_value_dicts":
            parsed_data[key] = (
                section_separator + section_separator.join(f"{k}: {v}" for item in value for k, v in item.items()) + closing_tag
            )

        else:
            parsed_data[key] = str(value)

    return parsed_data


def get_record_and_types_as_strings(data: Dict[str, Any], keys_to_parse: List[str]) -> Dict[str, str]:
    """
    Parses specific keys in a JSON dictionary into plain text, removing hyperlinks but keeping structure.
    """
    parsed_data = {}

    section_separator = ", "

    for key in keys_to_parse:
        if key not in data:
            continue

        value = data[key]["value"]
        data_type = data[key]["type"]

        if value is None:
            parsed_data[key] = ""
            continue

        if data_type == "link_list":
            parsed_data[key] = section_separator.join(item["label"] for item in value)

        elif data_type == "link_dict":
            parsed_data[key] = value["label"]

        elif data_type == "link_list_hierarchy":
            parsed_hierarchy = []
            for sublist in value:
                hierarchy_links = " > ".join(item["label"] for item in sublist)
                parsed_hierarchy.append(hierarchy_links)
            parsed_data[key] = ", ".join(parsed_hierarchy)

        elif data_type == "label_dict":
            parsed_data[key] = value["label"] if isinstance(value, dict) else ""
        elif data_type == "string":
            parsed_data[key] = str(value)
        elif data_type == "date":
            parsed_data[key] = str(value)
        elif data_type == "string_list":
            parsed_data[key] = section_separator.join(value) if isinstance(value, list) else ""
        elif data_type == "key_value_dicts":
            parsed_data[key] = section_separator.join(f"{k}: {v}" for item in value for k, v in item.items())
        else:
            parsed_data[key] = str(value)

    return parsed_data


def get_parsed_data_as_str(data: Dict[str, Any], keys_to_parse: List[str]) -> str:
    """
    Parses specific keys and returns the data as a single formatted string.
    """
    section_tag = "div"
    parsed_data = get_record_and_types_as_strings(data, keys_to_parse)

    html = ""

    for key, value in parsed_data.items():
        key_translated = translate("label_" + key)
        html += f"<{section_tag}><b>{key_translated} ({key})</b>: {value}</{section_tag}>"
    return html


def get_parsed_data_as_table(data: Dict[str, Any], keys_to_parse: List[str], debug: bool = False) -> str:
    """
    Parses specific keys and returns the data as a single formatted string.
    """
    parsed_data = get_record_and_types_as_strings(data, keys_to_parse)

    table_html = "<table>"
    for key, value in parsed_data.items():
        display_key = translate("label_" + key)
        if debug:
            display_key = f"{display_key} ({key})"
        table_html += f"<tr><td class='width-200'>{display_key}</td><td>{value}</td></tr>"
    table_html += "</table>"
    return table_html


def get_parsed_data_as_html(data: Dict[str, Any], keys_to_parse: List[str], section_tag: str = "p") -> str:
    """
    Parses specific keys and returns the data as a single html string.
    """
    parsed_data = get_record_and_types_as_html(data, keys_to_parse, section_tag)
    for key, value in parsed_data.items():
        key_translated = translate("label_" + key)
        parsed_data[key] = f"<div><b>{key_translated}</b>: {value}</div>"

    return "".join(parsed_data.values())
