def normalize_legal_restrictions(record: dict):
    """This is always displayed"""

    text = ""
    legal_id = record["legal_id"]
    if legal_id == 1:
        text = "Materialet er ikke underlagt andre juridiske begrænsninger af tilgængeligheden."
    elif legal_id == 2:
        text = "Materialet er utilgængeligt ifølge persondatalovgivningen."
    elif legal_id == 3:
        text = "Materialet er utilgængeligt ifølge arkivlovgivningen."
    elif legal_id == 4:
        text = "Materialet er utilgængeligt som følge af særlige juridiske forhold."

    record["other_legal_restrictions_normalized"] = text
    return record


__ALL__ = [normalize_legal_restrictions]


def _normalize_legal_restrictions(record: dict):
    legal_id = record["legal_id"]
    contractual_id = record["contractual_id"]
    availability_id = record["availability_id"]

    output_text = "Materialet er online her på Aarhusarkivet.dk, men det er det enkelte materiales ophavsretslige status, "
    output_text += "der fastsætter, hvad et givent materiale videre må bruges til."

    if legal_id > 1 or contractual_id == 1:
        output_text = "Materialet er utilgængeligt som følge af nævnte juridiske forhold."
    elif contractual_id == 2:
        output_text = "Materialet er kun tilgængeligt gennem ansøgning."
    elif availability_id == 2:
        output_text = "Materialet skal bestilles hjem til læsesalen, før det kan beses."
    elif availability_id == 3:
        output_text = "Materialet er tilgængeligt på læsesalen. Der kræves ikke forudgående bestilling for at se materialet på læsesalen. "
        output_text += "Man skal blot møde op i åbningstiderne."

    record["other_legal_restrictions_normalized"] = output_text
    return record
