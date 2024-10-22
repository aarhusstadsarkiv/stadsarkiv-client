"""
Format relations obtained from the proxies api.
"""

import re


def format_relations(type: str, relations: list):
    """
    Format relations obtained from the proxies api.
    Used with tearterakivet
    """

    onstage = []
    offstage = []
    for rel in relations:
        label: str = rel.get("rel_label")
        if label.startswith("Skuespiller") and label.find("("):
            start_index = label.find("(") + 1
            rel["rel_label"] = label[start_index:-1]
            onstage.append(rel)
        elif label.startswith("Skuespiller") or label.startswith("Statist"):
            onstage.append(rel)
        else:
            offstage.append(rel)

    return [
        {"label": "Sceneroller", "data": onstage},
        {"label": "Produktionshold", "data": offstage},
    ]


def sort_data(data: list, key: str):
    """
    Sorting is a mess. Sometimes "rel_date_from" is present when sorting by a date
    and sometime is is not. Best way to sort is to extract the year from the display_label.
    """

    def get_sort_key(item: dict):
        if key == "rel_label":
            return item.get("rel_label", "")
        elif key == "display_label":
            # Extract year from display_label, if present
            match = re.search(r"(\d{4})", item.get("display_label", ""))
            year = int(match.group(1)) if match else float("inf")  # Set to infinity if no year present
            return (year, item.get("display_label", ""))
        return ("",)  # Default return value

    sorted_data = []
    for section in data:
        if "data" in section:
            section["data"] = sorted(section["data"], key=get_sort_key)
        sorted_data.append(section)

    return sorted_data


def _sort_by_value(list_of_dicts: list, key_name: str, default=None):
    decorated = [(dict_.get(key_name, default), dict_) for dict_ in list_of_dicts]
    return [dict_ for (key, dict_) in decorated]
