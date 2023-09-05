from stadsarkiv_client.core.logging import get_log
from stadsarkiv_client.resources import normalize_fields


log = get_log()


def events_alter(event: dict):
    event = normalize_fields.set_sources_normalized(event)
    log.debug(event)
    # location = normalize_fields.set_latitude_longitude(location)
    event = normalize_fields.get_resource_and_types(event)

    return event
