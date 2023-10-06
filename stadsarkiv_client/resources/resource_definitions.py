"""
A mapping of resource key names to their definitions (type).
"""

resource_definitions = {
    # creators
    "date_from": {"type": "string"},
    "date_to": {"type": "string"},
    "description": {"type": "paragraphs"},
    "domain": {"type": "string"},
    "local_area": {"type": "string"},
    "gender": {"type": "string"},
    "firstnames": {"type": "string_list"},
    "lastnames": {"type": "string_list"},
    "occupation": {"type": "string_list"},
    "industry": {"type": "string_list"},
    "collectors_link": {"type": "link_list"},
    "creators_link": {"type": "link_list"},
    "sources_normalized": {"type": "string_list"},
    # people
    "content_and_scope": {"type": "paragraphs"},
    "date_of_birth": {"type": "string"},
    "date_of_death": {"type": "string"},
    "place_of_birth": {"type": "string"},
    "place_of_death": {"type": "string"},
    # collections
    "summary": {"type": "string"},
    "access": {"type": "paragraphs"},
    "legal_status": {"type": "paragraphs"},
    "level_of_digitisation": {"type": "paragraphs"},
    "citation": {"type": "paragraphs"},
    "custodial_history": {"type": "paragraphs"},
    "level_of_kassation": {"type": "paragraphs"},
    "accrual_status": {"type": "paragraphs"},
    "system_of_arrangement": {"type": "paragraphs"},
    "archival_history": {"type": "paragraphs"},
    "extent": {"type": "paragraphs"},
    "bulk_years": {"type": "paragraphs"},
    "accumulation_range": {"type": "paragraphs"},
    "outer_years": {"type": "string"},
    # locations
    "name": {"type": "string"},
    "addr_nr": {"type": "string"},
    "zipcode": {"type": "string"},
    "display_label": {"type": "string"},
    "latitude_longitude_normalized": {"type": "string"},
    "parish": {"type": "string"},
    "rotation": {"type": "string"},
    # events
    "ext_data": {"type": "key_value_dict"},
    "event_type": {"type": "string_list"},
    # collectors
    "portrait": {"type": "image"},
    "date_created": {"type": "string"},
    "date_decommissioned": {"type": "string"},
}
