import typing
import json
from pathlib import Path
import os


def load_facets():
    """
    Load facets from facets_imported.json.
    """
    dir_path = os.path.dirname(os.path.realpath(__file__))
    facets_file = Path(dir_path) / "facets_imported.json"
    with open(facets_file, "r", encoding="utf8") as f:
        facets = json.load(f)
    return facets


def replace_key(d):
    """
    Replace the key 'display_label' with 'label' in a dictionary.
    """
    if isinstance(d, dict):
        if "display_label" in d:
            d["label"] = d.pop("display_label")
        for key in d:
            replace_key(d[key])
    elif isinstance(d, list):
        for item in d:
            replace_key(item)


def add_id_to_list_of_dicts(list_of_dicts):
    """
    Add an id key to each dict in a list of dicts.
    """
    for dict in list_of_dicts:
        dict["id"] = dict["label"]


facets = load_facets()
replace_key(facets)
add_id_to_list_of_dicts(facets)

settings_facets: dict[str, typing.Any] = {
    "events": {
        "label": "Forestillinger",
        "type": "resource_links",
        "resource_type": "events",
        "content": facets,
    },
    "dates": {
        "label": "Datering",
        "type": "date_form",
        "content": [],
    },
}
