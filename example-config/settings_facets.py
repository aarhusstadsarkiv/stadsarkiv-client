FACETS = {
    "content_types": {
        "label": "Materialetype",
        "multiple": True,
        "hierarchical": True,
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
}
