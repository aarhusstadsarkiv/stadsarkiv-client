# convert a dict symbol from .py to yml
import yaml

from stadsarkiv_client.core.module_loader import load_submodule_from_file

# settings_facets = load_submodule_from_file("language", "language", "example-config-simple/language.py")
# with open("example-config-simple/language.yml", "w", encoding="utf8") as file:
#     yaml.dump(settings_facets, file, allow_unicode=True, sort_keys=True)