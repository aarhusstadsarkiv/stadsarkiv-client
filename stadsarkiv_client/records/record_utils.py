def is_collection(record_dict: dict, collection_id: int):
    """
    Check if the record belongs to a collection.
    """
    try:
        collection = record_dict["collection"].get("id")
    except KeyError:
        return False

    if collection == collection_id:
        return True

    return False


def is_curator(record_dict: dict, curator_id: int):
    """
    Check if first curator is the same as curator_id.
    """

    try:
        curator = record_dict["curators"][0]
    except KeyError:
        return False

    if curator["id"] == curator_id:
        return True

    return False
