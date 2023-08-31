from stadsarkiv_client.core.logging import get_log
from stadsarkiv_client.resources import normalize_fields


log = get_log()


def creators_alter(creator: dict):
    creator = normalize_fields.set_sources_normalized(creator)
    creator = normalize_fields.get_resource_and_types(creator)

    return creator
