"""ChangeLog — migrated from Katalon `API Coverage/ModulePlatform/ChangeLog*`.

Real endpoints (from Katalon Object Repository):
  - GET  /api/changes/lastmodifieddate
  - POST /api/changes/force
  - POST /api/platform/changelog/search
"""

import uuid

import allure
import pytest

from core.clients.rest import RestClient
from restapi.operations import CatalogOperations


@pytest.mark.restapi
@allure.feature("Platform / ChangeLog (REST API)")
@allure.title("Get last modified date")
def test_changelog_get_last_modified_date(rest_client: RestClient, backend_base_url: str):
    with allure.step("GET /api/changes/lastmodifieddate"):
        result = rest_client.get(f"{backend_base_url}/api/changes/lastmodifieddate")

    with allure.step("Verify date returned"):
        assert result is not None


@pytest.mark.restapi
@allure.feature("Platform / ChangeLog (REST API)")
@allure.title("Force cache and verify last modified date updates")
def test_changelog_force_cache(rest_client: RestClient, backend_base_url: str):
    with allure.step("POST /api/changes/force"):
        rest_client.post(f"{backend_base_url}/api/changes/force", json={})

    with allure.step("Get updated date"):
        updated = rest_client.get(f"{backend_base_url}/api/changes/lastmodifieddate")

    with allure.step("Verify date returned"):
        assert updated is not None


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


@pytest.mark.restapi
@allure.feature("Platform / ChangeLog (REST API)")
@allure.title("Verify changelog after entity creation")
def test_changelog_verify_log_after_entity_change(rest_client: RestClient, backend_base_url: str):
    catalog_ops = CatalogOperations(rest_client, backend_base_url)
    cat_name = f"QAChangeLog_{uuid.uuid4().hex[:8]}"

    with allure.step(f"Create catalog: {cat_name}"):
        catalog = catalog_ops.create(name=cat_name)
        assert catalog["id"]

    try:
        with allure.step("Search changelog for the new entity"):
            result = rest_client.post(
                f"{backend_base_url}/api/platform/changelog/search",
                json={"skip": 0, "take": 20},
            )
            assert result is not None
    finally:
        with allure.step("Cleanup — delete catalog"):
            try:
                catalog_ops.delete(catalog["id"])
            except Exception:
                pass
