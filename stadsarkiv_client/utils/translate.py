from stadsarkiv_client.utils.dynamic_settings import settings
from stadsarkiv_client.locales.en import en
from stadsarkiv_client.locales.da import da
from stadsarkiv_client.utils.logging import log
import json

try:
    from language import language as language_local
    log.info("Loaded local language file: language.py")
except ImportError:
    language_local = None


def translate(key) -> str | None:
    translation = None

    if key not in da:
        _add_translate_key_value('da', key)

    if key not in en:
        _add_translate_key_value('en', key)

    if settings["language"] == 'da':
        translation = _translate_local(key)
        if not translation:
            translation = da[key]

    if settings["language"] == 'en':
        translation = _translate_local(key)
        if not translation:
            translation = en[key]

    return translation


def _translate_local(key) -> str | None:
    translation = None

    if language_local:
        if key in language_local:
            translation = language_local[key]

    return translation


def _add_translate_key_value(lang, key) -> None:
    if lang == 'da':
        da[key] = key

        _save_file_dict('da')

    if lang == 'en':
        en[key] = key

        _save_file_dict('en')


def _save_file_dict(lang) -> None:

    if settings["environment"] == 'production':
        return

    if lang == 'en':
        with open("stadsarkiv_client/locales/en.py", 'w') as f:
            f.write(f"{lang} = " + json.dumps(en, indent=4, sort_keys=True, ))

    if lang == 'da':
        with open("stadsarkiv_client/locales/da.py", 'w') as f:
            f.write(f"{lang} = " + json.dumps(da, indent=4, sort_keys=True))
