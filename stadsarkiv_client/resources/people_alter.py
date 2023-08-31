from stadsarkiv_client.core.logging import get_log
from stadsarkiv_client.resources import normalize_fields


log = get_log()

# type_str = [
#     "description",
#     "content_and_scope",
#     "gender",
#     "date_of_birth",
#     "date_of_death",
#     "place_of_birth",
#     "place_of_death",
# ]

# lists = [
#     "firstnames",
#     "lastnames",
#     "occupation",
# ]


def people_alter(people: dict):
    people = normalize_fields.set_sources_normalized(people)
    people = normalize_fields.get_resource_and_types(people)

    return people
