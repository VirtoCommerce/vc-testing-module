"""Platform diagnostics — migrated from Katalon `API Coverage/ModulePlatform/Diagnostics*`."""

import allure
import pytest

from core.clients.rest import RestClient


@pytest.mark.restapi
@allure.feature("Platform / Diagnostics (REST API)")
@allure.title("Get system info")
def test_diagnostics_system_info(rest_client: RestClient, backend_base_url: str):
    with allure.step("GET /api/platform/diagnostics/systeminfo"):
        info = rest_client.get(f"{backend_base_url}/api/platform/diagnostics/systeminfo")

    with allure.step("Verify system info fields"):
        assert info is not None
        assert "is64BitProcess" in info


@pytest.mark.restapi
@allure.feature("Platform / Diagnostics (REST API)")
@allure.title("Get modules with errors")
def test_diagnostics_modules_with_errors(rest_client: RestClient, backend_base_url: str):
    with allure.step("GET /api/platform/diagnostics/moduleserrors"):
        errors = rest_client.get(f"{backend_base_url}/api/platform/diagnostics/moduleserrors")

    with allure.step("Verify empty errors list (healthy platform)"):
        assert errors is not None
        assert isinstance(errors, list)
        assert len(errors) == 0, f"Expected no module errors, got: {errors}"
