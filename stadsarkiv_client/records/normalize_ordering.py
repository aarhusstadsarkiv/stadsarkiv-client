"""
Normalize ordering (Bestilling)

"""

from stadsarkiv_client.core.logging import get_log
from stadsarkiv_client.core.translate import translate

log = get_log()


def normalize_ordering(record: dict):
    """Add ordering to record"""
    availability_id = record.get("availability_id", None)
    legal_id = record.get("legal_id", None)
    contractual_id = record.get("contractual_id", 0)
    curators: list = record.get("curators", [])

    result = []
    if availability_id == 2 and legal_id == 1 and contractual_id > 2:
        result.append(translate("ordering_by_mail"))
        for curator in curators:
            if curator.get("id") == 2:
                result.append(translate("ordering_from_rigsarkivet"))
            elif curator.get("id") == 4:
                result.append(translate("ordering_aarhus_teatret"))

    if result:
        record["ordering_normalized"] = result

    return record
