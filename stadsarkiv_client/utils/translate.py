from stadsarkiv_client.utils.dynamic_settings import settings
from stadsarkiv_client.locales.en import en
from stadsarkiv_client.locales.da import da
import json
from stadsarkiv_client.utils.logging import get_log

log = get_log()

try:
    from language import language as language_local

    log.info("Loaded local language file: language.py")
except ImportError:
    log.info("Local language file NOT loaded: language.py")
    language_local = None


def translate(key: str) -> str:
    translation = ''

    # Add key to language files if not exists
    if key not in da:
        _add_translate_key_value("da", key)

    if key not in en:
        _add_translate_key_value("en", key)

    # If local language file exists, use that. Else use default language
    if settings["language"] == "da":
        translation = _translate_local(key)
        if not translation:
            translation = da[key]

    if settings["language"] == "en":
        translation = _translate_local(key)
        if not translation:
            translation = en[key]

    return translation


def _translate_local(key: str) -> str | None:
    """ Get translation from local language file if exists"""
    translation = None

    if language_local:
        if key in language_local:
            translation = language_local[key]

    return translation


def _add_translate_key_value(lang, key) -> None:
    if lang == "da":
        da[key] = key

        _save_file_dict("da")

    if lang == "en":
        en[key] = key

        _save_file_dict("en")


def _save_file_dict(lang) -> None:
    if settings["environment"] == "production":
        return

    if lang == "en":
        file_contents_en = f"{lang} = {json.dumps(en, indent=4, sort_keys=True)}"
        with open("stadsarkiv_client/locales/en.py", "w") as f:
            f.write(file_contents_en)

    if lang == "da":
        file_contents_da = f"{lang} = {json.dumps(da, indent=4, sort_keys=True)}"
        with open("stadsarkiv_client/locales/da.py", "w") as f:
            f.write(file_contents_da)
