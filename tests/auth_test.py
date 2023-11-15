from stadsarkiv_client.app import app
from stadsarkiv_client.core.logging import get_log
from starlette.testclient import TestClient
import unittest

log = get_log()

test_user = "dennis.iversen@gmail.com"
test_password = "testtest"

correct_login = {"username": test_user, "password": test_password}
incorrect_login = data = {"username": "bad.mail@test.com", "password": "bad_password"}

log.info(f"test_user: {test_user}")
log.info(f"test_password: {test_password}")


class TestAuth(unittest.TestCase):
    def test_login_get(self):
        client = TestClient(app)
        response = client.get("/auth/login")
        self.assertEqual(response.status_code, 200)

    def test_login_correct_post(self):
        client = TestClient(app)
        response = client.post("/auth/login", data=correct_login, follow_redirects=True)  # type: ignore
        self.assertEqual(response.url, "http://testserver/")

    def test_login_incorrect_post(self):
        client = TestClient(app)
        response = client.post("/auth/login", data=incorrect_login, follow_redirects=True)  # type: ignore
        self.assertEqual(response.url, "http://testserver/auth/login?next=/")

    def test_logout_post(self):
        client = TestClient(app)
        response = client.post("/auth/logout", follow_redirects=True)
        self.assertEqual(response.url, "http://testserver/auth/login")

    def test_logout_get(self):
        client = TestClient(app)
        response = client.get("/auth/logout", follow_redirects=True)
        self.assertEqual(response.url, "http://testserver/auth/login?next=/auth/logout")

    def test_me_loggedin_get(self):
        client = TestClient(app)
        response = client.post("/auth/login", data=correct_login)  # type: ignore
        response = client.get("/auth/me")
        self.assertEqual(response.status_code, 200)

    def test_me_not_logged_in_get(self):
        client = TestClient(app)
        response = client.get("/auth/me", follow_redirects=True)
        self.assertEqual(response.url, "http://testserver/auth/login?next=/auth/me")

    def test_register_get(self):
        client = TestClient(app)
        response = client.get("/auth/register")
        self.assertEqual(response.status_code, 200)

    def test_register_post(self):
        client = TestClient(app)

        """
        User exists. At some point we should test with a user that does not exist.
        Before that is possible we should be allowed to delete a user from the database.
        """

        data = {"email": correct_login["username"], "password": correct_login["password"], "password_2": correct_login["password"]}
        response = client.post("/auth/register", data=data, follow_redirects=True)  # type: ignore
        self.assertEqual(response.url, "http://testserver/auth/register")

    def test_verify_get(self):
        client = TestClient(app)
        response = client.get("/auth/verify/fake-token")
        self.assertEqual(response.url, "http://testserver/")
