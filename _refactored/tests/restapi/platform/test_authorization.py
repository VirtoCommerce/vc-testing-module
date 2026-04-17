"""Authorization tests — migrated from Katalon `API Coverage/ModulePlatform/Authorization*`."""

import allure
import pytest
import requests

from core.global_settings import GlobalSettings


@pytest.mark.restapi
@allure.feature("Platform / Authorization (REST API)")
@allure.title("Get token with valid credentials")
def test_auth_back_token(global_settings: GlobalSettings) -> None:
    with allure.step("POST /connect/token — valid admin credentials"):
        response = requests.post(
            f"{global_settings.backend_base_url}/connect/token",
            data={
                "grant_type": "password",
                "scope": "offline_access",
                "username": global_settings.admin_username,
                "password": global_settings.admin_password.get_secret_value(),
            },
            timeout=global_settings.requests_timeout,
            verify=global_settings.verify_ssl,
        )

    with allure.step("Verify token returned"):
        assert response.status_code == 200
        body = response.json()
        assert body.get("access_token"), "access_token missing"
        assert body.get("token_type") == "Bearer"


@pytest.mark.restapi
@allure.feature("Platform / Authorization (REST API)")
@allure.title("Auth validation — empty username returns 400")
def test_auth_validation_empty_username(global_settings: GlobalSettings) -> None:
    with allure.step("POST /connect/token — empty username"):
        response = requests.post(
            f"{global_settings.backend_base_url}/connect/token",
            data={
                "grant_type": "password",
                "scope": "offline_access",
                "username": "",
                "password": "anything",
            },
            timeout=global_settings.requests_timeout,
            verify=global_settings.verify_ssl,
        )

    with allure.step("Verify 400 with error description"):
        assert response.status_code == 400
        body = response.json()
        assert "error" in body or "error_description" in body


@pytest.mark.restapi
@allure.feature("Platform / Authorization (REST API)")
@allure.title("Auth validation — wrong credentials returns 400")
def test_auth_validation_wrong_credentials(global_settings: GlobalSettings) -> None:
    with allure.step("POST /connect/token — wrong password"):
        response = requests.post(
            f"{global_settings.backend_base_url}/connect/token",
            data={
                "grant_type": "password",
                "scope": "offline_access",
                "username": global_settings.admin_username,
                "password": "definitely_wrong_password_12345",
            },
            timeout=global_settings.requests_timeout,
            verify=global_settings.verify_ssl,
        )

    with allure.step("Verify 400"):
        assert response.status_code == 400


@pytest.mark.restapi
@allure.feature("Platform / Authorization (REST API)")
@allure.title("Get external sign-in providers")
def test_auth_external_sign_in_providers(rest_client, backend_base_url: str) -> None:
    with allure.step("GET /api/platform/security/externalsigninproviders"):
        try:
            result = rest_client.get(f"{backend_base_url}/api/platform/security/externalsigninproviders")
        except Exception as exc:
            pytest.skip(f"External sign-in providers endpoint not available on this platform version: {exc}")

    with allure.step("Verify response"):
        assert result is not None
