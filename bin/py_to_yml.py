# convert a dict symbol from .py to yml
import yaml
import typing


from stadsarkiv_client.core.module_loader import load_submodule_from_file

settings = load_submodule_from_file("settings", "settings", "example-config-aarhus/settings.py")

# with open("example-config-aarhus/settings.yml", "w", encoding="utf8") as file:
#     yaml.dump(settings, file, allow_unicode=True, sort_keys=True)

# settings_facets = load_submodule_from_file("settings", "settings", "example-config-demo/settings.py")
# with open("example-config-demo/settings.yml", "w", encoding="utf8") as file:
#     yaml.dump(settings_facets, file, allow_unicode=True, sort_keys=True)

settings_facets = load_submodule_from_file("facets", "settings_facets", "example-config-simple/facets.py")
with open("example-config-simple/facets.yml", "w", encoding="utf8") as file:
    yaml.dump(settings_facets, file, allow_unicode=True, sort_keys=True)
