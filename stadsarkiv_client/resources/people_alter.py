from stadsarkiv_client.core.logging import get_log
from stadsarkiv_client.resources import normalize_fields


log = get_log()


def people_alter(people: dict):
    people = normalize_fields.set_sources_normalized(people)
    people = normalize_fields.get_resource_and_types(people)

    return people
