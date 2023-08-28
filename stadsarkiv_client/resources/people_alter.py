from stadsarkiv_client.core.logging import get_log
from stadsarkiv_client.resources import normalize_fields


log = get_log()

type_str = [
    "description",
    "content_and_scope",
    "gender",
    "date_of_birth",
    "date_of_death",
    "place_of_birth",
    "place_of_death",
]

lists = [
    "firstnames",
    "lastnames",
    "occupation",
]


def _list_to_type_list(name: str, value: list):
    return {
        "type": "string_list",
        "value": value,
        "name": name,
    }


def _str_to_type_str(name: str, value: str):
    return {
        "type": "paragraphs",
        "value": value,
        "name": name,
    }


def people_alter(people: dict):
    for elem in type_str:
        if elem in people:
            people[elem] = _str_to_type_str(elem, people[elem])

    for elem in lists:
        if elem in people:
            people[elem] = _list_to_type_list(elem, people[elem])

    if "sources" in people:
        people["sources"] = normalize_fields.get_sources_normalized(people["sources"])

    people = normalize_fields.set_outer_years(people)
    return people
