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


def people_alter(people: dict):
    for elem in type_str:
        if elem in people:
            people[elem] = normalize_fields.str_to_type_str(elem, people[elem])

    for elem in lists:
        if elem in people:
            people[elem] = normalize_fields.list_to_type_list(elem, people[elem])

    if "sources" in people:
        people["sources"] = normalize_fields.get_sources_normalized(people["sources"])

    people = normalize_fields.set_outer_years(people)
    return people
