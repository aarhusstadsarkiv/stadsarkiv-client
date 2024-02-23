from stadsarkiv_client.app import app
from stadsarkiv_client.core.logging import get_log
from starlette.testclient import TestClient
import unittest

log = get_log()

valid_user = "dennis.iversen@gmail.com"
valid_password = "testtest"

invalid_user = "bad.mail@test.com"
invalid_password = "bad_password"

correct_login = {"username": valid_user, "password": valid_password}
incorrect_login = {"username": invalid_user, "password": invalid_password}


"""
User already exists. At some point we should test with a user that does not exist.
Before that is possible we should be allowed to delete a user from the database.
So some of these tests are a bit shallow.
"""


class TestAuth(unittest.TestCase):
    def test_login_get(self):
        client = TestClient(app)
        response = client.get("/auth/login")
        self.assertEqual(response.status_code, 200)

    def test_login_post_correct(self):
        client = TestClient(app)
        response = client.post("/auth/login", data=correct_login, follow_redirects=True)  # type: ignore
        self.assertEqual(response.url, "http://testserver/")

    def test_login_post_incorrect(self):
        client = TestClient(app)
        response = client.post("/auth/login", data=incorrect_login, follow_redirects=True)  # type: ignore
        self.assertEqual(response.url, "http://testserver/auth/login?next=/search")

    def test_logout_get(self):
        client = TestClient(app)
        response = client.get("/auth/logout", follow_redirects=True)
        self.assertEqual(response.url, "http://testserver/auth/login?next=/auth/logout")

    def test_logout_post(self):
        client = TestClient(app)
        response = client.post("/auth/logout", follow_redirects=True)
        self.assertEqual(response.url, "http://testserver/auth/login")

    def test_register_get(self):
        client = TestClient(app)
        response = client.get("/auth/register")
        self.assertEqual(response.status_code, 200)

    def test_register_post(self):
        client = TestClient(app)
        data = {"email": correct_login["username"], "password": correct_login["password"], "password_2": correct_login["password"]}
        response = client.post("/auth/register", data=data, follow_redirects=True)  # type: ignore
        self.assertEqual(response.url, "http://testserver/auth/register")

    def test_forgot_password_get(self):
        client = TestClient(app)
        response = client.get("/auth/forgot-password")
        self.assertEqual(response.status_code, 200)

    # def test_forgot_password_post(self):
    #     client = TestClient(app)
    #     response = client.post("/auth/forgot-password", data={"email": valid_user}, follow_redirects=True)  # type: ignore
    #     self.assertEqual(response.url, "http://testserver/auth/forgot-password")

    def test_reset_password_get(self):
        client = TestClient(app)
        response = client.get("/auth/reset-password/fake-token")
        self.assertEqual(response.status_code, 200)

    def test_reset_password_post(self):
        client = TestClient(app)
        response = client.post(
            "/auth/reset-password/fake-token", data={"password": valid_password, "password_2": valid_password}, follow_redirects=True
        )
        self.assertEqual(response.url, "http://testserver/auth/reset-password/fake-token")

    def test_verify_get(self):
        client = TestClient(app)
        response = client.get("/auth/verify/fake-token")
        self.assertEqual(response.url, "http://testserver/")

    def test_me_loggedin_get(self):
        client = TestClient(app)
        response = client.post("/auth/login", data=correct_login)  # type: ignore
        response = client.get("/auth/me")
        self.assertEqual(response.status_code, 200)

    def test_me_not_logged_in_get(self):
        client = TestClient(app)
        response = client.get("/auth/me", follow_redirects=True)
        self.assertEqual(response.url, "http://testserver/auth/login?next=/auth/me")
