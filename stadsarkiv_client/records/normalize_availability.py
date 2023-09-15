from stadsarkiv_client.core.translate import translate


def normalize_availability(record: dict):
    """
    Add availability_normalized to record
    """
    legal_id = record["legal_id"]
    contractual_id = record["contractual_id"]
    availability_id = record["availability_id"]

    output_text = translate("availability_common")

    if legal_id > 1 or contractual_id == 1:
        output_text = translate("availability_contractual_id_1")
    elif contractual_id == 2:
        output_text = translate("availability_contractual_id_2")
    elif availability_id == 2:
        output_text = translate("availability_availability_id_2")
    elif availability_id == 3:
        output_text = translate("availability_availability_id_3")

    record["availability_normalized"] = output_text
    return record
