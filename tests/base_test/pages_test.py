"""
Test of some resources and records
"""

from maya.app import app
from maya.core.logging import get_log
from starlette.testclient import TestClient
import os
import unittest

log = get_log()

test_user = os.getenv("TEST_USER", "")
test_password = os.getenv("TEST_PASSWORD", "")


class TestPages(unittest.TestCase):
    def test_not_found_get(self):
        client = TestClient(app)
        response = client.get("/not_found")
        self.assertEqual(response.status_code, 404)

    def test_home_get(self):
        client = TestClient(app)
        response = client.get("/")
        self.assertEqual(response.status_code, 200)

    def test_collections(self):
        client = TestClient(app)
        response = client.get("/collections/1")
        self.assertEqual(response.status_code, 200)

    def test_people(self):
        client = TestClient(app)
        response = client.get("/people/000116683")
        self.assertEqual(response.status_code, 200)

    def test_locations(self):
        client = TestClient(app)
        response = client.get("/locations/24421")
        self.assertEqual(response.status_code, 200)

    def test_creators(self):
        client = TestClient(app)
        response = client.get("/creators/109847")
        self.assertEqual(response.status_code, 200)

    def test_events(self):
        client = TestClient(app)
        response = client.get("/events/111818")
        self.assertEqual(response.status_code, 200)

    def test_organisations(self):
        client = TestClient(app)
        response = client.get("/organisations/107438")
        self.assertEqual(response.status_code, 200)

    def test_collectors(self):
        client = TestClient(app)
        response = client.get("/collectors/100701")
        self.assertEqual(response.status_code, 200)

    def test_record(self):
        client = TestClient(app)
        response = client.get("/records/000316141")
        self.assertEqual(response.status_code, 200)

    def test_record_audio(self):
        client = TestClient(app)
        response = client.get("/records/000466994")
        self.assertEqual(response.status_code, 200)

    def test_event_teater(self):
        client = TestClient(app)
        response = client.get("/events/112281")
        self.assertEqual(response.status_code, 200)
