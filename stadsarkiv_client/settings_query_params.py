"""
This file contains the settings query parameters that can be used in the
search query.
"""

from types import MappingProxyType


def make_immutable(obj):
    """
    Recursively convert all dicts inside obj to MappingProxyType.
    """
    if isinstance(obj, dict):
        return MappingProxyType({k: make_immutable(v) for k, v in obj.items()})
    return obj


settings_query_params = {
    "view": {
        "label": "Visning",
        "repeatable": False,
        "type": "string",
        "search_filter": False,
    },
    "fmt": {
        "label": "Format",
        "repeatable": False,
        "type": "string",
        "search_filter": False,
    },
    "sort": {
        "label": "Sortering",
        "repeatable": False,
        "type": "string",
        "search_filter": False,
    },
    "direction": {
        "label": "Retning",
        "repeatable": False,
        "type": "string",
        "search_filter": False,
    },
    "size": {
        "label": "Antal visninger",
        "repeatable": False,
        "type": "integer",
        "search_filter": False,
    },
    "start": {
        "label": "Start",
        "repeatable": False,
        "type": "integer",
        "search_filter": False,
    },
    "q": {
        "label": "Fritekstsøgning",
        "repeatable": False,
        "type": "string",
        "negatable": False,
        "search_filter": True,
    },
    "date_from": {
        "label": "Tidligste dato",
        "repeatable": False,
        "type": "date",
        "negatable": False,
        "search_filter": True,
    },
    "date_to": {
        "label": "Seneste dato",
        "repeatable": False,
        "type": "date",
        "negatable": False,
        "search_filter": True,
    },
    # entities
    "creators": {
        "label": "Ophavsretsholder",
        "repeatable": True,
        "type": "object",
        "negatable": True,
        "search_filter": True,
        "entity": True,
    },
    "locations": {
        "label": "Stedsangivelse",
        "repeatable": True,
        "type": "object",
        "negatable": True,
        "search_filter": True,
        "entity": True,
    },
    "events": {
        "label": "Begivenhed",
        "repeatable": True,
        "type": "object",
        "negatable": True,
        "search_filter": True,
        "entity": True,
    },
    "people": {
        "label": "Person",
        "repeatable": True,
        "type": "object",
        "negatable": True,
        "search_filter": True,
        "entity": True,
    },
    "organisations": {
        "label": "Organisation",
        "repeatable": True,
        "type": "object",
        "negatable": True,
        "search_filter": True,
        "entity": True,
    },
    "collection": {
        "label": "Samling",
        "repeatable": False,
        "type": "object",
        "negatable": True,
        "search_filter": True,
        "entity": True,
        "entity_path": "collections",
    },
    "collectors": {
        "label": "Arkivskaber",
        "repeatable": True,
        "type": "object",
        "negatable": True,
        "search_filter": True,
        "entity": True,
    },
    "subjects": {
        "label": "Emnekategori",
        "repeatable": True,
        "type": "object",
        "negatable": True,
        "search_filter": True,
    },
    "series": {
        "label": "Arkivserie",
        "repeatable": False,
        "type": "string",
        "negatable": False,
        "search_filter": True,
    },
    "admin_tags": {
        "label": "Administrativt tag",
        "repeatable": True,
        "type": "string",
        "negatable": True,
        "search_filter": True,
    },
    "collection_tags": {
        "label": "Samlingstags",
        "repeatable": True,
        "type": "string",
        "negatable": True,
        "search_filter": True,
    },
    "content_types": {
        "label": "Materialetype",
        "repeatable": True,
        "type": "object",
        "negatable": True,
        "search_filter": True,
    },
    "curators": {
        "label": "Kurator",
        "repeatable": True,
        "type": "object",
        "negatable": True,
        "search_filter": True,
        "entity": True,
        # if label_only is True then the entity can not be displayed
        "label_only": True,
    },
    "availability": {
        "label": "Tilgængelighed",
        "repeatable": False,
        "type": "object",
        "negatable": True,
        "search_filter": True,
    },
    "usability": {
        "label": "Hvad må jeg bruge?",
        "repeatable": False,
        "type": "object",
        "negatable": True,
        "search_filter": True,
    },
    "registration_id": {
        "label": "RegistreringsID",
        "repeatable": False,
        "type": "integer",
        "negatable": False,
        "search_filter": True,
    },
    "cursor": {
        "label": "Næste resultat",
        "repeatable": False,
        "type": "string",
        "negatable": False,
        "search_filter": False,
    },
    "utm_source": {
        # "label": "Næste resultat",
        "repeatable": False,
        "type": "string",
        "negatable": False,
        "search_filter": False,
    },
    "utm_campaign": {
        # "label": "Næste resultat",
        "repeatable": False,
        "type": "string",
        "negatable": False,
        "search_filter": False,
    },
    "utm_medium": {
        # "label": "Næste resultat",
        "repeatable": False,
        "type": "string",
        "negatable": False,
        "search_filter": False,
    },
}

settings_query_params = make_immutable(settings_query_params)
