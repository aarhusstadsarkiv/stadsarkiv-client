"""
File contains functions for altering resources,
e.g. set sources_normalized, set outer years, etc.
"""

from stadsarkiv_client.core.logging import get_log
from stadsarkiv_client.resources import normalize_fields


log = get_log()


def resource_alter(resource: dict):
    schema = resource["schema"]

    if schema == "collection":
        resource = collections_alter(resource)
    elif schema == "organisation":
        resource = organisations_alter(resource)
    elif schema == "collector":
        resource = collectors_alter(resource)
    elif schema == "creator":
        resource = creators_alter(resource)
    elif schema == "event":
        resource = events_alter(resource)
    elif schema == "address" or schema == "place":
        resource = locations_alter(resource)
    elif schema == "person":
        resource = person_alter(resource)
    else:
        raise Exception(f"Unknown schema: {schema}")

    return resource


def collections_alter(collection: dict):
    collection = normalize_fields.set_sources_normalized(collection)
    collection = normalize_fields.set_outer_years(collection)
    collection = normalize_fields.get_resource_and_types(collection)

    # These are either string_list or link_list.
    string_list_or_link_list = [
        "collectors",
        "curators",
    ]

    for elem in string_list_or_link_list:
        if elem in collection:
            collection[elem] = normalize_fields.get_string_or_link_list(elem, collection[elem])

    return collection


def organisations_alter(organisation: dict):
    schema = "organisation"
    organisation = normalize_fields.set_created_decommissioned(organisation)
    organisation = normalize_fields.set_collectors_link_list(organisation, schema)
    organisation = normalize_fields.set_creators_link_list(organisation, schema)
    organisation = normalize_fields.set_sources_normalized(organisation)
    organisation = normalize_fields.get_resource_and_types(organisation)

    # These are either string_list or link_list.
    string_list_or_link_list = [
        "collectors",
        "curators",
    ]

    for elem in string_list_or_link_list:
        if elem in organisation:
            organisation[elem] = normalize_fields.get_string_or_link_list(elem, organisation[elem])

    return organisation


def collectors_alter(collector: dict):
    schema = collector["schema"]
    if schema == "organisation":
        collector = normalize_fields.set_created_decommissioned(collector)

    collector = normalize_fields.set_collectors_link_list(collector, schema)
    collector = normalize_fields.set_creators_link_list(collector, schema)
    collector = normalize_fields.set_sources_normalized(collector)
    collector = normalize_fields.get_resource_and_types(collector)

    # These are either string_list or link_list.
    string_list_or_link_list = [
        "collectors",
        "curators",
    ]

    for elem in string_list_or_link_list:
        if elem in collector:
            collector[elem] = normalize_fields.get_string_or_link_list(elem, collector[elem])

    return collector


def creators_alter(creator: dict):
    schema = creator["schema"]
    if schema == "organisation":
        creator = normalize_fields.set_created_decommissioned(creator)
    creator = normalize_fields.set_collectors_link_list(creator, schema)
    creator = normalize_fields.set_creators_link_list(creator, schema)
    creator = normalize_fields.set_sources_normalized(creator)
    creator = normalize_fields.get_resource_and_types(creator)

    return creator


def events_alter(event: dict):
    event = normalize_fields.set_sources_normalized(event)
    event = normalize_fields.get_resource_and_types(event)
    return event


def locations_alter(location: dict):
    location = normalize_fields.set_sources_normalized(location)
    location = normalize_fields.set_latitude_longitude(location)
    location = normalize_fields.get_resource_and_types(location)
    return location


def person_alter(people: dict):
    people = normalize_fields.set_sources_normalized(people)
    people = normalize_fields.get_resource_and_types(people)
    return people
