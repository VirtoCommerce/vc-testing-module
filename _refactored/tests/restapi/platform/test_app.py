"""Platform apps — basic smoke test."""

import allure
import pytest

from core.clients.rest import RestClient


@pytest.mark.restapi
@allure.feature("Platform / Apps (REST API)")
@allure.title("List installed platform apps")
def test_platform_apps(rest_client: RestClient, backend_base_url: str):
    with allure.step("GET /api/platform/apps"):
        apps = rest_client.get(f"{backend_base_url}/api/platform/apps")

    with allure.step("Verify non-empty response"):
        assert apps is not None, "Platform apps are None"
        assert len(apps) > 0, "Platform apps are empty"
