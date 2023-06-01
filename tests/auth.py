from starlette.responses import HTMLResponse
from starlette.testclient import TestClient
import sys
import os
import unittest

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from stadsarkiv_client.app import app


class TestStringMethods(unittest.TestCase):
    def test_upper(self):
        self.assertEqual("foo".upper(), "FOO")

    def test_home(self):
        client = TestClient(app)
        response = client.get("/")
        self.assertEqual(response.status_code, 200)
