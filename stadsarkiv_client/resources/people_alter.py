"""
{
  "description": "Kontorassistent ved Erhvervsarkivet.",
  "display_label": "Preben Rasmussen",
  "domain": "people",
  "firstnames": [
    "Preben"
  ],
  "gender": "mand",
  "id": "000151936",
  "is_creator": true,
  "lastnames": [
    "Rasmussen"
  ],
  "occupation": [
    "Kontorassistent"
  ],
  "schema": "person",
  "version_nr": 1
}

{
  "date_of_birth": "1913",
  "date_of_death": "1996",
  "display_label": "John Price (1913-1996)",
  "domain": "people",
  "firstnames": [
    "John Christopher Valdemar"
  ],
  "gender": "mand",
  "id": "000121365",
  "lastnames": [
    "Price"
  ],
  "occupation": [
    "Instrukt\u00f8r",
    "Skuespiller"
  ],
  "place_of_birth": "K\u00f8benhavn",
  "place_of_death": "K\u00f8benhavn",
  "schema": "person",
  "sources": [
    "https://da.wikipedia.org/wiki/John_Price",
    "http://denstoredanske.dk/Dansk_Biografisk_Leksikon/Kunst_og_kultur/Teater_og_film/Skuespiller/John_Price"
  ]
}

"""


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

string_link_list = [
    "sources",
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

    for elem in string_link_list:
        if elem in people:
            people[elem] = normalize_fields.get_string_or_link_list(elem, people[elem])

    people = normalize_fields.set_outer_years(people)
    return people
