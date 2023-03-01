from stadsarkiv_client.utils.dynamic_settings import settings
from stadsarkiv_client.locales.en import en
from stadsarkiv_client.locales.da import da
import json


def translate(key) -> str | None:
    translation = None

    if key not in da:
        _add_translate_key_value('da', key)

    if key not in en:
        _add_translate_key_value('en', key)

    if settings["language"] == 'da':
        translation = da[key]

    if settings["language"] == 'en':
        translation = en[key]

    return translation


def _add_translate_key_value(lang, key) -> None:
    if lang == 'da':
        da[key] = key

        _save_file_dict('da')

    if lang == 'en':
        en[key] = key

        _save_file_dict('en')


def _save_file_dict(lang) -> None:
    if lang == 'en':
        with open(f"stadsarkiv_client/locales/en.py", 'w') as f:
            f.write(f"{lang} = " + json.dumps(en, indent=4, sort_keys=True))

    if lang == 'da':
        with open(f"stadsarkiv_client/locales/da.py", 'w') as f:
            f.write(f"{lang} = " + json.dumps(da, indent=4, sort_keys=True))
