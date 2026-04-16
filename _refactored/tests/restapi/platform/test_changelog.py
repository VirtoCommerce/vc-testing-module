"""ChangeLog — migrated from Katalon `API Coverage/ModulePlatform/ChangeLog*`."""

import allure
import pytest

from core.clients.rest import RestClient


@pytest.mark.restapi
@allure.feature("Platform / ChangeLog (REST API)")
@allure.title("Get last modified date")
def test_changelog_get_last_modified_date(rest_client: RestClient, backend_base_url: str):
    with allure.step("GET /api/platform/changelog/lastmodifieddate"):
        result = rest_client.get(f"{backend_base_url}/api/platform/changelog/lastmodifieddate")

    with allure.step("Verify date returned"):
        assert result is not None


@pytest.mark.restapi
@allure.feature("Platform / ChangeLog (REST API)")
@allure.title("Search changelog entries")
def test_changelog_search(rest_client: RestClient, backend_base_url: str):
    with allure.step("POST /api/platform/changelog/search"):
        result = rest_client.post(
            f"{backend_base_url}/api/platform/changelog/search",
            json={"skip": 0, "take": 10},
        )

    with allure.step("Verify response structure"):
        assert result is not None
        assert "results" in result or "totalCount" in result
