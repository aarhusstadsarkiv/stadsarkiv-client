from .logging import get_log


log = get_log()


creative_commons_link = '<a href="https://creativecommons.org/licenses/by/4.0/deed.da">Creative Commons Navngivelse licens</a>'
special_notice = "Stadsarkivet modtager gerne oplysninger, som kan hjælpe med at identificere den hidtil ukendte ophavsmand/-kvinde. "


def _get_special_notice_id(record: dict):
    try:
        id = record["content_types"][0][0].get("id")
    except Exception:
        id = None

    if id != 36:
        return True

    return False


def normalize_copyright(record: dict):
    log.debug(record)

    lines = []

    label = record["copyright_status"].get("label")
    lines.append(label)

    copyright_id = record["copyright_id"]
    if copyright_id == 1:
        text = "Materialet har ikke værkshøjde og er derfor ikke beskyttet af ophavsret. "
        text += "Der er dermed heller ingen ophavsretslige begrænsninger på gengivelse og publicering af dette materiale. "
        lines.append(text)

    if copyright_id == 2:
        text = "Materialet er i offentlig eje, da ophavsretten er udløbet. "
        text += "Der er dermed heller ingen ophavsretslige begrænsninger på gengivelse og publicering af dette materiale. "
        lines.append(text)

    if copyright_id == 3:
        text = "Materialet er frigivet af alle ophavsretsholdere til offentlig eje. "
        text += "Der er dermed heller ingen ophavsretslige begrænsninger på gengivelse og publicering af dette materiale. "
        lines.append(text)

    if copyright_id == 4:
        text = f"Materialet er under ophavsret, men udgives efter aftale under en {creative_commons_link}. "
        text += "Materialet må derfor gerne gengives og publiceres, så længe man på passende vis krediterer både ophavsmanden/-kvinden og AarhusArkivet.dk "
        lines.append(text)

    if copyright_id == 5:
        text = f"Materialet er under ophavsret, men udgives efter aftale under en {creative_commons_link}. "
        text += "Materialet må kun gengives og publiceres i ikke-kommercielle sammenhænge, og under forudsætning af en passende kreditering af både ophavsmanden/-kvinden og AarhusArkivet.dk. "
        text += "Dette udelukker publicering på sociale platforme som Facebook og Instagram. "
        lines.append(text)

    if copyright_id == 6:
        text = "Ophavsretsaftalen kræver alle rettigheder forbeholdt. "
        text += "Materialet må derfor hverken gengives eller publiceres andetsteds. "
        lines.append(text)

    if copyright_id == 7:
        text = "En eller flere nødvendige ophavsretsaftaler mangler, ofte på grund af ukendte skabere eller rettighedshavere. "
        text = "Materialet må derfor hverken gengives eller publiceres andetsteds. "
        lines.append(text)

    if copyright_id == 8:
        text = "Vi har endnu ikke undersøgt materialets ophavsretslige forhold. "
        text += "Materialet må derfor hverken gengives eller publiceres andetsteds. "
        lines.append(text)

    if copyright_id == 9:
        text = "Materialets ophavsretslige status er undersøgt, men stadig uafklaret. "
        text += "Materialet må derfor hverken gengives eller publiceres andetsteds. "
        lines.append(text)

    if copyright_id in [7, 8, 9]:
        if _get_special_notice_id(record):
            lines.append(special_notice)

    record["copyright_status_normalized"] = lines
    return record


__ALL__ = [normalize_copyright]
