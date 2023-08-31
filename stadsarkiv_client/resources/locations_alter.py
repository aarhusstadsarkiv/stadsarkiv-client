from stadsarkiv_client.core.logging import get_log
from stadsarkiv_client.resources import normalize_fields


log = get_log()


def locations_alter(location: dict):
    location = normalize_fields.set_sources_normalized(location)
    location = normalize_fields.set_latitude_longitude(location)
    location = normalize_fields.get_resource_and_types(location)

    return location
