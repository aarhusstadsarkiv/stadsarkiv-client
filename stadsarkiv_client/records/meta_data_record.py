"""
Get some usefull meta data for a record
"""

from stadsarkiv_client.core.logging import get_log
from starlette.requests import Request
from stadsarkiv_client.core.translate import translate
from stadsarkiv_client.core.hooks import get_hooks
import typing


hooks = get_hooks()
log = get_log()


IP_ALLOW = ["193.33.148.24"]


ICONS = {
    "61": {"icon": "image", "label": "Billeder"},
    "95": {"icon": "laptop_mac", "label": "Elektronisk materiale"},
    "10": {"icon": "gavel", "label": "Forskrifter og vedtægter"},
    "1": {"icon": "folder_open", "label": "Kommunale sager og planer"},
    "75": {"icon": "map", "label": "Kortmateriale"},
    "49": {"icon": "description", "label": "Manuskripter"},
    "87": {"icon": "movie", "label": "Medieproduktioner"},
    "81": {"icon": "audio_file", "label": "Musik og lydoptagelser"},
    "36": {"icon": "menu_book", "label": "Publikationer"},
    "18": {"icon": "local_library", "label": "Registre og protokoller"},
    "29": {"icon": "bar_chart", "label": "Statistisk og økonomisk materiale"},
    "99": {"icon": "description", "label": "Andet materiale"},
}


def get_record_meta_data(request: Request, record: dict) -> dict[str, typing.Any]:
    """Get usefull meta data for a record"""
    meta_data = {}

    meta_data["allowed_by_ip"] = _is_allowed_by_ip(request)
    meta_data["title"] = _get_record_title(record)
    meta_data["meta_title"] = _get_record_meta_title(record)
    meta_data["icon"] = _get_icon(record)

    meta_data["copyright_id"] = record["copyright_status"].get("id")
    meta_data["legal_id"] = record["other_legal_restrictions"].get("id")
    meta_data["contractual_id"] = record["contractual_status"].get("id")
    meta_data["availability_id"] = record["availability"].get("id")
    meta_data["usability_id"] = record["usability"].get("id")

    # This should be altered to record_represenation_type
    meta_data = _set_representations(meta_data, record)

    meta_data["is_downloadable"] = _is_downloadable(meta_data)
    return meta_data


def _is_allowed_by_ip(request: Request) -> bool:
    try:
        ip = request["client"][0]
    except KeyError:
        return False

    if ip in IP_ALLOW:
        return True
    return False


def _get_icon(record: dict):
    """Get icon for the record based on content type"""
    try:
        content_type_id = record["content_types"][0][0]["id"]
        icon = ICONS[str(content_type_id)]
    except KeyError:
        icon = ICONS["99"]

    return icon


def _is_sejrs_sedler(record_dict: dict):
    if "collection" not in record_dict:
        return False

    if record_dict["collection"].get("id") == 1:
        return True

    return False


def _is_downloadable(metadata: dict) -> bool:
    return (
        metadata.get("representations", False)
        and metadata["legal_id"] == 1
        and metadata["contractual_id"] > 3
        and metadata["usability_id"] in [1, 2, 3]
        and metadata["record_type"] != "video"
    )


def _get_record_title(record_dict: dict):
    title = translate("No title")
    record_title = record_dict.get("title")
    if not record_title:
        record_title = record_dict.get("heading")

    if record_title:
        title = record_title

    return title


def _set_representations(meta_data: dict, record: dict):
    meta_data["record_type"] = "unknown"
    if "representations" in record:
        meta_data["record_type"] = record["representations"].get("record_type", "unknown")

    meta_data["has_representations"] = False
    if meta_data["legal_id"] == 1 and meta_data["contractual_id"] > 2:
        meta_data["has_representations"] = True

    meta_data["is_representations_online"] = False
    if meta_data["availability_id"] == 4 or meta_data["allowed_by_ip"]:
        meta_data["is_representations_online"] = True

    if _is_sejrs_sedler(record):
        meta_data["record_type"] = "sejrs_sedler"

    return meta_data


def _get_record_meta_title(record_dict: dict):
    title = _get_record_title(record_dict)
    title = hooks.get_record_meta_title(title)

    if _is_sejrs_sedler(record_dict):
        if record_dict.get("summary"):
            title = record_dict["summary"][:60]
            title = f"[{title}... | AarhusArkivet ]"

    return title
