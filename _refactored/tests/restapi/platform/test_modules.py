"""Modules management — migrated from Katalon `API Coverage/ModulePlatform/ModulesManagement`."""

import allure
import pytest

from core.clients.rest import RestClient


@pytest.mark.restapi
@allure.feature("Platform / Modules (REST API)")
@allure.title("Get installed modules")
def test_modules_get_installed(rest_client: RestClient, backend_base_url: str) -> None:
    with allure.step("GET /api/platform/modules"):
        modules = rest_client.get(f"{backend_base_url}/api/platform/modules")

    with allure.step("Verify modules list"):
        assert isinstance(modules, list)
        assert len(modules) > 0
        ids = [m.get("id", "") for m in modules]
        assert any("VirtoCommerce.Catalog" in mid for mid in ids), f"Expected Catalog module, got: {ids[:5]}..."


@pytest.mark.restapi
@allure.feature("Platform / Modules (REST API)")
@allure.title("Reload modules")
@pytest.mark.serial
def test_modules_reload(rest_client: RestClient, backend_base_url: str) -> None:
    with allure.step("POST /api/platform/modules/reload"):
        rest_client.post(f"{backend_base_url}/api/platform/modules/reload", json={})

    with allure.step("Verify modules still available"):
        modules = rest_client.get(f"{backend_base_url}/api/platform/modules")
        assert isinstance(modules, list)
        assert len(modules) > 0
