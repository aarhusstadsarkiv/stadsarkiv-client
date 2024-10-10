import os
import json


def generate_import_map(base_dir):
    js_files = [f for f in os.listdir(base_dir) if f.endswith(".js")]
    import_map = {"imports": {}}

    for js_file in js_files:
        # key = "{{ url_for('static', path='/js/" + js_file + "') }}"
        # value = key + "?v={{ get_setting('version') }}"
        key = f"/static/js/{js_file}"
        value = key + "?v={{ get_setting('version') }}"
        import_map["imports"][key] = value

    return json.dumps(import_map, indent=4)


base_directory = "stadsarkiv_client/static/js"
import_map = generate_import_map(base_directory)

import_map_html = f'<script type="importmap">\n{import_map}\n</script>'
with open("stadsarkiv_client/templates/includes/importmap.html", "w") as f:
    f.write(import_map_html)
