def normalize_contractual_status(record, creators=None):

    contractual_id = record.get('contractual_id')

    text = ''
    if contractual_id == 1:
        text = "Materialet er utilgængeligt. Ifølge aftale."
    elif contractual_id == 2:
        text = "Materialet er kun tilgængeligt gennem ansøgning. Ifølge aftale."
    elif contractual_id == 3:
        text = "Materialet må kun ses på læsesalen. Ifølge aftale."
    elif contractual_id == 4:

        creators = {'pp': False}

        if record.get('creators'):
            for i in record.get('creators'):
                if i.get('id') == 108691:
                    creators.update({'pp': True})

        if creators['pp']:
            text = "Materialet må kun offentliggøres på Aarhus Stadsarkivs hjemmesider. Ifølge aftale."
        else:
            text = "Materialet må offentliggøres på internettet. Ifølge aftale."
    else:
        text = "Materialet er ikke begrænset af kontraktuelle klausuler."

    # return text
    record["contractual_status_normalized"] = text
    return record


__ALL__ = [normalize_contractual_status]
