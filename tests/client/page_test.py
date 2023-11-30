"""
Test of some modified resources on "teater" client. 
"""

from stadsarkiv_client.app import app
from stadsarkiv_client.core.logging import get_log
from starlette.testclient import TestClient
import unittest

log = get_log()


class TestAuth(unittest.TestCase):
    def test_event_teater(self):
        client = TestClient(app)
        response = client.get("/events/112281")
        self.assertEqual(response.status_code, 200)
