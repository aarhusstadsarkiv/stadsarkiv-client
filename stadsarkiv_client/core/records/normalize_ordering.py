from ..logging import get_log


log = get_log()


def normalize_ordering(record: dict):
    availability_id = record.get("availability_id", None)
    legal_id = record.get("legal_id", None)
    contractual_id = record.get("contractual_id", 0)
    curators: list = record.get("curators", [])

    result = []
    if availability_id == 2 and legal_id == 1 and contractual_id > 2:
        result.append(
            "Du kan bestille materialet ved at sende en mail til stadsarkiv@aarhus.dk "
            "hvori du angiver materialets arkiv-ID, som kan ses øverst på siden."
        )
        for curator in curators:
            if curator.get("id") == 2:
                result.append(
                    "Hvis materialet ligger hos Rigsarkivet, skal bestillingen sendes dertil. "
                    "Gå ind på Rigsarkivets hjemmeside og find materialet der. "
                    "Efterfølgende kan det så bestilles hjem til en af deres læsesale."
                )
            elif curator.get("id") == 4:
                result.append("Materialet kan ses på Aarhus Teaters Arkiv.")
        result.append("")

    if result:
        record["ordering"] = result

    return record


__ALL__ = [normalize_ordering]
