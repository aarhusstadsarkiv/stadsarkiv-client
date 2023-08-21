from stadsarkiv_client.core.logging import get_log

log = get_log()


def _has_abstract(collection: dict):
    abstract = ["summary", "description", "content_and_scope"]
    for key in abstract:
        if key in collection:
            return True

    return False


def _has_access_usage(collection: dict):
    access_usage = ["access", "legal_status", "level_of_digitisation", "citation"]

    for key in access_usage:
        if key in collection:
            return True

    return False


def _has_history(collection: dict):
    history = ["custodial_history", "level_of_kassation", "accrual_status"]

    for key in history:
        if key in collection:
            return True

    return False


def _has_litteratur(collection: dict):
    litterature = ["sources"]
    for key in litterature:
        if key in collection:
            return True

    return False


def _has_series(collection: dict):
    if "series" in collection and len(collection["series"]) > 0:
        return True

    return False


def _has_collection_tags(collection: dict):
    if "collection_tags" in collection and len(collection["collection_tags"]) > 0:
        return True

    return False


def _has_highlights(collection: dict):
    if "highlights" in collection and len(collection["highlights"]) > 0:
        return True

    return False


def get_collection_meta_data(collection: dict):
    meta_data = {}
    # meta_data["has_abstract"] = _has_abstract(collection)
    meta_data["has_access_usage"] = _has_access_usage(collection)
    meta_data["has_history"] = _has_history(collection)
    meta_data["has_litteratur"] = _has_litteratur(collection)
    meta_data["has_series"] = _has_series(collection)
    meta_data["has_collection_tags"] = _has_collection_tags(collection)
    meta_data["has_highlights"] = _has_highlights(collection)

    return meta_data
