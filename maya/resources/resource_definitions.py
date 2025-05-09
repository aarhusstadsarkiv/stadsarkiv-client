"""
A mapping of resource key names to their definitions (type).
"""

resource_definitions = {
    # creators
    "date_from": {"type": "string"},
    "date_to": {"type": "string"},
    "description": {"type": "paragraphs"},
    # "domain": {"type": "string"},
    "local_area": {"type": "string"},
    "gender": {"type": "string"},
    "firstnames": {"type": "string_list_as_string"},
    "lastnames": {"type": "string_list_as_string"},
    "occupation": {"type": "string_list"},
    "industry": {"type": "string_list"},
    "collectors": {"type": "link_list"},
    "curators": {"type": "link_list"},
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
    "latitude_longitude_normalized": {"type": "latitude_longitude_normalized"},
    "parish": {"type": "string"},
    "rotation": {"type": "string"},
    # events
    "event_type": {"type": "string_list"},
    "ext_data": {"type": "key_value_dict"},
    # specific for teaterarkivet
    "ext_data_season": {"type": "string"},
    "ext_data_playwright": {"type": "string"},
    "ext_data_original_id": {"type": "string"},
    "ext_data_stagename": {"type": "string"},
    "ext_data_production": {"type": "string"},
    "ext_data_arkiv_id": {"type": "string"},
    "ext_data_number_of_performances": {"type": "string"},
    "ext_data_translater": {"type": "string"},
    "date_from_premier": {"type": "string"},
    "persons_links": {"type": "link_list"},
    # collectors
    "portrait": {"type": "image"},
    "date_created": {"type": "string"},
    "date_decommissioned": {"type": "string"},
    "alt_names": {"type": "string_list"},
    # slideshow
    "highlights": {"type": "slideshow"},
    "series": {"type": "tree"},
    "collection_tags": {"type": "tree"},
}
