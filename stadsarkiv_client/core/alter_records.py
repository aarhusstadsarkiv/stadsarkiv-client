from stadsarkiv_client.core.logging import get_log
import urllib.parse


log = get_log()


def list_dict_id_label(original_data):
    """
    Transform the following data:
    original_data = [{"id": [1, 2, 3], "label": ["a", "b", "c"]}]
    transformed_data = [{"id": 1, "label": "a"}, {"id": 2, "label": "b"}, {"id": 3, "label": "c"}]
    """
    transformed_data = [
        {"id": item["id"][index], "label": item["label"][index]}
        for item in original_data for index in range(len(item["id"]))
    ]
    return transformed_data


def normalize_series(record: dict):
    """
    create a series_normalized dict with collection_id and series list
    """

    if "series" in record and "collection" in record:
        # split string series into list using '/' as separator
        series_normalized = []

        series_list = record["series"].split("/")
        collection_id = record["collection"]["id"]

        query = 'collection=' + str(collection_id) + '&series='
        for series in series_list:

            # if not first or last in series add '/' to query
            if series != series_list[0] and series != series_list[-1]:
                query += urllib.parse.quote('/')

            query += urllib.parse.quote(series)
            entry = {"collection": collection_id, "series": series, "query": query}
            series_normalized.append(entry)

        record["series_normalized"] = series_normalized
    return record


def alter_record(record: dict):

    record = normalize_series(record)
    convert_to_list_of_dicts = ["subjects", "content_types"]

    for key, value in record.items():
        if key in convert_to_list_of_dicts:
            record[key] = list_dict_id_label(value)

    return record
