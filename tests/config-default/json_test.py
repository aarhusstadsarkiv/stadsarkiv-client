"""
Test of JSON response
"""

from stadsarkiv_client.app import app
from stadsarkiv_client.core.logging import get_log
from starlette.testclient import TestClient
import unittest
import json

log = get_log()


class TestJSON(unittest.TestCase):
    def test_readingroom(self):
        client = TestClient(app)
        url = "/records/000309478/json/meta_data"
        response = client.get(url)
        json_response = response.json()

        json_expected = r"""
{
  "id": "000309478",
  "real_id": "309478",
  "allowed_by_ip": false,
  "title": "Aarhus Vejviser 1997",
  "meta_title": "Aarhus Vejviser 1997",
  "meta_description": "",
  "icon": {
    "icon": "description",
    "label": "Andet materiale"
  },
  "copyright_id": 7,
  "legal_id": 1,
  "contractual_id": 5,
  "availability_id": 3,
  "usability_id": 4,
  "collection_id": 204,
  "content_types_label": "",
  "is_representations_online": false,
  "is_downloadable": false
}
    """
        # parse json
        json_expected = json.loads(json_expected)
        self.assertEqual(json_response, json_expected)

    def test_pdf(self):
        client = TestClient(app)
        url = "/records/000182391/json/meta_data"
        response = client.get(url)
        json_response = response.json()

        json_expected = r"""
{
  "id": "000182391",
  "real_id": "182391",
  "allowed_by_ip": false,
  "title": "Salgsbrochure for kampagne Byg og bo i Aarhus.",
  "meta_title": "Salgsbrochure for kampagne Byg og bo i Aarhus.",
  "meta_description": "",
  "icon": {
    "icon": "description",
    "label": "Andet materiale"
  },
  "copyright_id": 4,
  "legal_id": 1,
  "contractual_id": 4,
  "availability_id": 4,
  "usability_id": 2,
  "collection_id": 194,
  "content_types_label": "",
  "is_representations_online": true,
  "record_type": "web_document",
  "representations": {
    "record_type": "web_document",
    "web_document_url": "https://acastorage.blob.core.windows.net/sam-access/000182391/000182391_c.pdf",
    "record_image": "https://acastorage.blob.core.windows.net/sam-access/000182391/000182391_m.jpg",
    "large_image": "https://acastorage.blob.core.windows.net/sam-access/000182391/000182391_m.jpg"
  },
  "portrait": "https://acastorage.blob.core.windows.net/sam-access/000182391/000182391_m.jpg",
  "is_downloadable": true
}
"""

        # parse json
        json_expected = json.loads(json_expected)
        self.assertEqual(json_response, json_expected)

    def test_video(self):
        client = TestClient(app)
        url = "/records/000313141/json/meta_data"
        response = client.get(url)
        response_json = response.json()

        # Define expected JSON using a raw string to avoid issues with escape characters
        json_expected = r"""
{
    "id": "000313141",
    "real_id": "313141",
    "allowed_by_ip": false,
    "title": "En køretur med sporvogn",
    "meta_title": "En køretur med sporvogn",
    "meta_description": "Filmens første 38 sekunder er fra Clemens Bro i 1902 \n\nDen 7. juli 1904 blev den første sporvognsrute indviet i Aarhus....",
    "icon": {
        "icon": "description",
        "label": "Andet materiale"
    },
    "copyright_id": 2,
    "legal_id": 1,
    "contractual_id": 5,
    "availability_id": 4,
    "usability_id": 1,
    "collection_id": null,
    "content_types_label": "",
    "is_representations_online": true,
    "record_type": "video",
    "representations": {
        "record_type": "video",
        "record_file": "https://acastorage.blob.core.windows.net/sam-access/000313141/000313141.mp4",
        "vimeo_id": "49234056",
        "record_image": "https://acastorage.blob.core.windows.net/sam-access/000313141/000313141_m.jpg",
        "large_image": "https://acastorage.blob.core.windows.net/sam-access/000313141/000313141_m.jpg"
    },
    "portrait": "https://acastorage.blob.core.windows.net/sam-access/000313141/000313141_m.jpg",
    "is_downloadable": false
}
        """

        json_expected = json.loads(json_expected)
        self.assertEqual(response_json, json_expected)
