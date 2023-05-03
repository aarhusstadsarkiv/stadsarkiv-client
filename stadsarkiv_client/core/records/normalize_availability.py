def normalize_availability(record: dict):
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

    record["availability_normalized"] = output_text
    return record


__ALL__ = [normalize_availability]
