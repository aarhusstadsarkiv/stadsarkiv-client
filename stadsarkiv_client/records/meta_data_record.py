"""
Get some usefull meta data for a record
"""

from stadsarkiv_client.core.logging import get_log
from starlette.requests import Request
from stadsarkiv_client.records import record_utils


log = get_log()


IP_ALLOW = ["193.33.148.24"]


ICONS = {
    "61": {"icon": "image", "label": "Billeder"},
    "95": {"icon": "laptop_windows", "label": "Elektronisk materiale"},
    "10": {"icon": "gavel", "label": "Forskrifter og vedtægter"},
    "1": {"icon": "folder_open", "label": "Kommunale sager og planer"},
    "75": {"icon": "map", "label": "Kortmateriale"},
    "49": {"icon": "description", "label": "Manuskripter"},
    "87": {"icon": "movie", "label": "Medieproduktioner"},
    "81": {"icon": "audio_file", "label": "Musik og lydoptagelser"},
    "36": {"icon": "article", "label": "Publikationer"},
    "18": {"icon": "menu_book", "label": "Registre og protokoller"},
    "29": {"icon": "bar_chart", "label": "Statistisk og økonomisk materiale"},
    "99": {"icon": "description", "label": "Andet materiale"},
}


def _strip_pre_zeroes(value: str) -> str:
    """
    Strip pre zeroes from a string
    """
    return value.lstrip("0")


def get_record_meta_data(request: Request, record: dict) -> dict:
    """
    Get usefull meta data for a record
    """
    meta_data = {}

    title = _get_record_title(record)
    if not title:
        quote_title = record_utils.meaningful_substring(record.get("summary", ""), 200)
        title = f"[{quote_title}]"

    meta_data["id"] = record["id"]
    meta_data["real_id"] = _strip_pre_zeroes(record["id"])
    meta_data["allowed_by_ip"] = _is_allowed_by_ip(request)
    meta_data["title"] = title
    meta_data["meta_title"] = _get_meta_title(record)
    meta_data["meta_description"] = record_utils.meaningful_substring(record.get("summary", ""), 120)
    meta_data["icon"] = _get_icon(record)
    meta_data["copyright_id"] = record["copyright_status"].get("id")
    meta_data["legal_id"] = record["other_legal_restrictions"].get("id")
    meta_data["contractual_id"] = record["contractual_status"].get("id")
    meta_data["availability_id"] = record["availability"].get("id")
    meta_data["usability_id"] = record["usability"].get("id")
    meta_data["collection_id"] = record.get("collection", {}).get("id")
    meta_data["series"] = record.get("series")
    meta_data["content_types"] = _get_content_type_label(record)
    # This should be altered to record_represenation_type
    meta_data = _set_representations(meta_data, record)

    meta_data["is_downloadable"] = _is_downloadable(meta_data)
    return meta_data


def _is_allowed_by_ip(request: Request) -> bool:
    try:
        ip = request["client"][0]
    except KeyError:
        return False
    except TypeError:
        return False

    if ip in IP_ALLOW:
        return True
    return False


def _get_icon(record: dict):
    """
    Get icon for the record based on content type
    content-types is in this format: [{'id': [10], 'label': ['Forskrifter og vedtægter']}]
    """
    try:
        content_type = record["content_types"][0]
        content_type_id = str(content_type["id"][0])
        return ICONS[content_type_id]
    except (KeyError, IndexError, TypeError):
        return ICONS["99"]


def _is_downloadable(meta_data: dict) -> bool:
    return (
        meta_data.get("representations", False)
        and meta_data["legal_id"] == 1
        and meta_data["contractual_id"] > 3
        and meta_data["usability_id"] in [1, 2, 3]
        and meta_data["record_type"] != "video"
    )


def _get_record_title(record: dict):
    """
    Try to get a title for the record. This is used as the title of the document, not the meta title
    """

    title = ""
    record_title = record.get("title")
    if not record_title:
        record_title = record.get("heading")

    if record_title:
        title = record_title

    return title


def _get_content_type_label(record: dict):
    # 'content_types': [{'id': [49, 55], 'label': ['Manuskripter', 'Udklip og småtryk']}],
    # Return it as a string, e.g. "Manuskripter > Udklip og småtryk"
    content_types = record.get("content_types", [])
    content_type_labels = []
    for content_type in content_types:
        content_type_labels.extend(content_type.get("label", []))

    return " > ".join(content_type_labels)



def _get_meta_title(record: dict):
    """
    Get the meta title for the record. This is used as the meta title of the document, the <title> tag
    """
    meta_title = _get_record_title(record)

    if not meta_title:
        meta_title = record_utils.meaningful_substring(record.get("summary", ""), 60)

    return meta_title


def _set_representations(meta_data: dict, record: dict):
    """
    This indicates if the record has representations, which images, audio, video, pdf, sejrs_sedler
    """

    meta_data["record_type"] = None
    if "representations" in record:
        meta_data["record_type"] = record["representations"].get("record_type")
        meta_data["representations"] = record["representations"]

        # Sometimes there is not a "large_image". Set "record_image" as "large_image" in that case
        if "large_image" not in meta_data["representations"]:
            meta_data["representations"]["large_image"] = meta_data["representations"].get("record_image")

        meta_data["portrait"] = record.get("portrait")

    meta_data["has_representations"] = False
    if meta_data["legal_id"] == 1 and meta_data["contractual_id"] > 2:
        meta_data["has_representations"] = True

    meta_data["is_representations_online"] = False
    if meta_data["availability_id"] == 4 or meta_data["allowed_by_ip"]:
        meta_data["is_representations_online"] = True

    # sejrs_sedler does not have a "representations" key, but it is a representation (text)
    # get the "collection" dict from the record and extract the "id" from it
    collection_id = record.get("collection", {}).get("id")
    if collection_id == 1:
        meta_data["record_type"] = "sejrs_sedler"
        meta_data["is_representations_online"] = True
        meta_data["has_representations"] = True

    return meta_data
