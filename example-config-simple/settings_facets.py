from stadsarkiv_client.core.logging import get_log
import typing

log = get_log()

settings_facets: dict[str, typing.Any] = {
    "content_types": {
        "label": "Materialetype",
        "type": "default",
        "content": [
            {"id": "99", "label": "Andet materiale"},
            {
                "children": [
                    {
                        "id": "66",
                        "icon": "far fa-image",
                        "label": "Afbildning af arkitektur og bygning",
                    },
                    {
                        "id": "65",
                        "icon": "far fa-image",
                        "label": "Afbildning af kunst",
                    },
                ],
                "id": "61",
                "icon": "far fa-image",
                "label": "Billeder",
            },
            {
                "children": [
                    {"id": "98", "icon": "fas fa-laptop", "label": "Hjemmesider"},
                    {"id": "96", "icon": "fas fa-laptop", "label": "Software"},
                    {"id": "97", "icon": "fas fa-laptop", "label": "Spil"},
                ],
                "id": "95",
                "icon": "fas fa-laptop",
                "label": "Elektronisk materiale",
            },
        ],
    },
    "events": {
        "label": "Forestillinger",
        "type": "resource_links",
        "resource_type": "events",
        "content": [
            {
                "label": "Sæson 2015-16",
                "children": [
                    {"label": "Imagine", "id": "118731"},
                    {"label": "Frk. Julie", "id": "118689"},
                ],
            },
            {
                "label": "Sæson 2016-17",
                "children": [
                    {"label": "American Spirit", "id": "119843"},
                    {"label": "En kvinde uden betydning", "id": "119569"},
                ],
            },
            {
                "label": "Sæson 2017-18",
                "children": [
                    {"id": "149860", "label": "Lyden af de skuldre vi står på"},
                    {"id": "149881", "label": "Fragt"},
                ],
            },
            {"label": "Sæson 2018-19", "children": [{"label": "Friheden", "id": "150474"}, {"label": "Revolution", "id": "150478"}]},
            {
                "label": "Sæson 2019-20",
                "children": [
                    {"label": "Lazarus", "id": "154644"},
                    {"label": "Pagten", "id": "154814"},
                    {"label": "Denungewertherslidelser", "id": "154899"},
                    {"label": "Lyden af de skuldre vi står på", "id": "154907"},
                    {"label": "Ordet", "id": "154912"},
                    {"label": "Se dagens lys", "id": "154654"},
                ],
            },
        ],
    },
}


def add_id_to_list_of_dicts(list_of_dicts):
    """
    Add an id key to each dict in a list of dicts.
    """
    for dict in list_of_dicts:
        dict["id"] = dict["label"]


events = settings_facets["events"]["content"]
add_id_to_list_of_dicts(events)
