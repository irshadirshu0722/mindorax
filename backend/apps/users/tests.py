from django.test import Client, TestCase
from unittest.mock import patch


class GoogleAuthApiTest(TestCase):
    def setUp(self):
        self.client = Client()

    @patch("apps.users.controller.TokenService.create_refresh_token")
    @patch("apps.users.controller.TokenService.create_access_token")
    @patch("apps.users.controller.GoogleAuthService.login_or_create_user")
    def test_google_login_returns_access_and_refresh_tokens(
        self,
        mock_login_or_create_user,
        mock_create_access_token,
        mock_create_refresh_token,
    ):
        mock_login_or_create_user.return_value = type("User", (), {"id": 1})()
        mock_create_access_token.return_value = "access-token"
        mock_create_refresh_token.return_value = "refresh-token"

        response = self.client.post(
            "/api/auth/google-login",
            data={"id_token": "fake-google-id-token"},
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(),
            {
                "access_token": "access-token",
                "refresh_token": "refresh-token",
            },
        )   

        mock_login_or_create_user.assert_called_once_with("fake-google-id-token")
        mock_create_access_token.assert_called_once_with(1)
        mock_create_refresh_token.assert_called_once_with(1)

    def test_refresh_token_missing_cookie(self,):
        response = self.client.get('/api/auth/refresh')
        assert response.status_code == 401
        assert response.json()['error'] == "Refresh token missing"
    
    @patch("apps.users.services.TokenService.refresh_access_token")
    def test_refresh_token_success(self,mock_refresh_access_token):
        mock_refresh_access_token.return_value = "new_access_token"
        response = self.client.get('/api/auth/refresh',HTTP_COOKIE="refresh_token=valid_token")
        assert response.status_code == 200
        assert response.json()["access_token"] == "new_access_token"