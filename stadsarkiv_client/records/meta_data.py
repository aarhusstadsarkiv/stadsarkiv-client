from stadsarkiv_client.core.logging import get_log
from starlette.requests import Request
from stadsarkiv_client.core.translate import translate


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


def is_allowed_by_ip(request: Request) -> bool:
    ip = request["client"][0]
    if ip in IP_ALLOW:
        return True
    return False


def _set_icon(record: dict):
    """Set icon for the record based on content type"""
    try:
        content_type_id = record["content_types"][0][0]["id"]
        record["icon"] = ICONS[str(content_type_id)]
    except KeyError:
        record["icon"] = ICONS["99"]

    return record


def _is_sejrs_sedler(record_dict: dict):
    if "collection" not in record_dict:
        return False

    if record_dict["collection"].get("id") == 1:
        return True

    return False


def set_representation_variables(record: dict):
    # Set record_type if record.representations exists
    record["record_type"] = None
    if "representations" in record:
        record["record_type"] = record["representations"].get("record_type")

    record["has_representations"] = False
    if record["legal_id"] == 1 and record["contractual_id"] > 2:
        # Then it is a representation, image, audio, video, web_document - or notice about reading room
        record["has_representations"] = True

    record["is_representations_online"] = False
    if record["availability_id"] == 4 or record["allowed_by_ip"]:
        record["is_representations_online"] = True

    if _is_sejrs_sedler(record):
        record["record_type"] = "sejrs_sedler"

    return record


def set_download_variables(record: dict) -> dict:
    record["is_downloadable"] = (
        record.get("representations")
        and record["legal_id"] == 1
        and record["contractual_id"] > 3
        and record["usability_id"] in [1, 2, 3]
        and record["record_type"] != "video"
    )
    return record


def set_common_variables(record: dict):
    record = _set_icon(record)

    # Set other keys in record dict
    record["copyright_id"] = record["copyright_status"].get("id")
    record["legal_id"] = record["other_legal_restrictions"].get("id")
    record["contractual_id"] = record["contractual_status"].get("id")
    record["availability_id"] = record["availability"].get("id")
    record["usability_id"] = record["usability"].get("id")

    return record


def set_record_title(record_dict: dict):
    title = translate("No title")
    record_title = record_dict.get("title")
    if not record_title:
        record_title = record_dict.get("heading")

    if record_title:
        title = record_title

    record_dict["title"] = title
    return record_dict


def get_meta_data(request: Request, record: dict):
    record["allowed_by_ip"] = is_allowed_by_ip(request)
    record = set_record_title(record)
    record = set_common_variables(record)
    record = set_representation_variables(record)
    record = set_download_variables(record)
    return record
