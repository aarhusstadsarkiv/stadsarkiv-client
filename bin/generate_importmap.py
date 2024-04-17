import os
import json


def generate_import_map(base_dir):
    js_files = [f for f in os.listdir(base_dir) if f.endswith(".js")]
    import_map = {"imports": {}}

    template = "{{{{ url_for('static', path='/js/{}') }}}}: {{{{ url_for('static', path='/js/{}') }}}}?v={{{{ get_setting('version') }}}}"
    for js_file in js_files:
        key = template.format(js_file, js_file).split(":")[0]
        value = template.format(js_file, js_file).split(":")[1]
        import_map["imports"][key] = value

    return json.dumps(import_map, indent=4)


base_directory = "stadsarkiv_client/static/js"
import_map = generate_import_map(base_directory)
print(import_map)
