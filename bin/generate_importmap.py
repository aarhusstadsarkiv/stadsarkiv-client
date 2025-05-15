#!/usr/bin/env python
import os
import json


def generate_import_map(base_dir):
    js_files = [f for f in os.listdir(base_dir) if f.endswith(".js")]
    import_map = {"imports": {}}

    for js_file in js_files:
        key = f"/static/js/{js_file}"
        value = key + "?v={{ get_setting('version') }}"
        import_map["imports"][key] = value

    return json.dumps(import_map, indent=4)


base_directory = "maya/static/js"
import_map = generate_import_map(base_directory)

import_map_html = f'<script type="importmap">\n{import_map}\n</script>'
with open("maya/templates/includes/importmap.html", "w") as f:
    f.write(import_map_html)
