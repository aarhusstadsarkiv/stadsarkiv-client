#!/usr/bin/env python

# convert a dict symbol from .py to yml
import yaml

from stadsarkiv_client.core.module_loader import load_submodule_from_file

settings_facets = load_submodule_from_file("language", "language", "example-config-teater/language.py")
with open("example-config-teater/language.yml", "w", encoding="utf8") as file:
    yaml.dump(settings_facets, file, allow_unicode=True, sort_keys=True)

# settings_facets = load_submodule_from_file("language", "da", "stadsarkiv_client/locales/da.py")
# with open("stadsarkiv_client/locales/da.yml", "w", encoding="utf8") as file:
#     yaml.dump(settings_facets, file, allow_unicode=True, sort_keys=True)

# settings_facets = load_submodule_from_file("language", "en", "stadsarkiv_client/locales/en.py")
# with open("stadsarkiv_client/locales/en.yml", "w", encoding="utf8") as file:
#     yaml.dump(settings_facets, file, allow_unicode=True, sort_keys=True)
