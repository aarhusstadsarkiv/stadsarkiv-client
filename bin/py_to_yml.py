# convert a dict symbol from .py to yml
import yaml

from stadsarkiv_client.core.module_loader import load_submodule_from_file

settings_facets = load_submodule_from_file("facets", "settings_facets", "example-config-simple/facets.py")
with open("example-config-simple/facets.yml", "w", encoding="utf8") as file:
    yaml.dump(settings_facets, file, allow_unicode=True, sort_keys=True)
