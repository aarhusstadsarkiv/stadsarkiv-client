import json
import os
from pathlib import Path

# load facets_imported.json as json
dir_path = os.path.dirname(os.path.realpath(__file__))
facets_file = Path(dir_path) / "facets_imported.json"
with open(facets_file, "r", encoding="utf8") as f:
    facets = json.load(f)


def replace_key(d):
    """
    Replace the key 'display_label' with 'label' in a dictionary.
    """
    if isinstance(d, dict):
        if 'display_label' in d:
            d['label'] = d.pop('display_label')
        for key in d:
            replace_key(d[key])
    elif isinstance(d, list):
        for item in d:
            replace_key(item)


replace_key(facets)

# save facets.json
facets_save_as = Path(dir_path) / "facets.json"
with open(facets_save_as, "w", encoding="utf8") as f:
    json.dump(facets, f, ensure_ascii=False, indent=4)
