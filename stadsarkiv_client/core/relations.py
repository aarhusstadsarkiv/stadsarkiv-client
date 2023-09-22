"""
Format relations obtained from the proxies api.
"""

from stadsarkiv_client.core.logging import get_log


log = get_log()


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

    if type in ["people"]:
        onstage_sorted = _sort_by_value(onstage, "rel_date_from", "2020-12-12")
        offstage_sorted = _sort_by_value(offstage, "rel_date_from", "2020-12-12")
    else:
        onstage_sorted = _sort_by_value(onstage, "rel_label")
        offstage_sorted = _sort_by_value(offstage, "rel_label")

    return [
        {"label": "Sceneroller", "data": onstage_sorted},
        {"label": "Produktionshold", "data": offstage_sorted},
    ]


# def sort_data(input_data):
#     sorted_data = []
#     for section in input_data:
#         sorted_section = dict(section)  # Create a copy of the section dictionary
#         sorted_section["data"] = sorted(section["data"], key=lambda x: x["rel_label"])
#         sorted_data.append(sorted_section)
#     return sorted_data


def _sort_by_value(list_of_dicts: list, key_name: str, default=None):
    decorated = [(dict_.get(key_name, default), dict_) for dict_ in list_of_dicts]
    return [dict_ for (key, dict_) in decorated]
