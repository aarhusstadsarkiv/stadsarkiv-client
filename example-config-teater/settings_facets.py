from stadsarkiv_client.core.logging import get_log
import typing
import json
from pathlib import Path
import os

log = get_log()

dir_path = os.path.dirname(os.path.realpath(__file__))
facets_file = Path(dir_path) / "facets.json"

with open(facets_file, "r", encoding="utf8") as f:
    facets = json.load(f)

settings_facets: dict[str, typing.Any] = {
    "events": {
        "label": "Forestillinger",
        "type": "resource_links",
        "resource_type": "events",
        "allow_facet_removal": True,  # default is to ignore a facet in settings_facets as a filter
        "content": facets,
    },
    "dates": {
        "label": "Datering",
        "type": "date_form",
        "content": [],
    },
}


def add_id_to_list_of_dicts(list_of_dicts):
    """
    Add an id key to each dict in a list of dicts.
    """
    for dict in list_of_dicts:
        dict["id"] = dict["label"]


events = settings_facets["events"]["content"]
add_id_to_list_of_dicts(events)
