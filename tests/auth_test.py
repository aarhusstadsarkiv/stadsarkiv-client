from stadsarkiv_client.app import app
from stadsarkiv_client.core.logging import get_log
import sys

from starlette.responses import HTMLResponse
from starlette.testclient import TestClient

import os
import unittest

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


log = get_log()


class TestAuth(unittest.TestCase):
    def test_home(self):
        client = TestClient(app)
        response = client.get("/")
        self.assertEqual(response.status_code, 200)

    def test_not_found(self):
        client = TestClient(app)
        response = client.get("/not_found")
        self.assertEqual(response.status_code, 404)

    def test_login(self):
        client = TestClient(app)
        response = client.get("/auth/login")
        self.assertEqual(response.status_code, 200)

    def test_login_post_correct(self):
        client = TestClient(app)
        response = client.post("/auth/post-login-jwt", data={"username": "dennis.iversen@gmail.com", "password": "iversen1234"})
        self.assertEqual(response.status_code, 200)

    def test_login_post_incorrect(self):
        client = TestClient(app)
        response = client.post("/auth/post-login-jwt", data={"username": "dennis.iversens@gmail.com", "password": "iversen1234"})
        self.assertEqual(response.status_code, 200)
