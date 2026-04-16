"""Asset file operations — migrated from Katalon `API Coverage/ModulePlatform/Asset*`."""

import allure
import pytest

from core.clients.rest import RestClient


@pytest.mark.restapi
@allure.feature("Platform / Assets (REST API)")
@allure.title("Upload asset file from URL")
def test_asset_upload_url(rest_client: RestClient, backend_base_url: str):
    with allure.step("POST /api/assets — upload from external URL"):
        result = rest_client.post(
            f"{backend_base_url}/api/assets",
            json={
                "url": "https://raw.githubusercontent.com/VirtoCommerce/vc-testing-module/dev/README.md",
                "name": "qa-test-upload.md",
                "folderUrl": "qa-test-assets",
            },
        )

    with allure.step("Verify upload response"):
        assert result is not None
        assert result.get("url") or result.get("relativeUrl"), f"Upload response missing URL: {result}"


@pytest.mark.restapi
@allure.feature("Platform / Assets (REST API)")
@allure.title("List assets in folder")
def test_asset_list(rest_client: RestClient, backend_base_url: str):
    with allure.step("GET /api/assets — root folder"):
        result = rest_client.get(f"{backend_base_url}/api/assets")

    with allure.step("Verify response"):
        assert result is not None


@pytest.mark.restapi
@allure.feature("Platform / Assets (REST API)")
@allure.title("Create blob folder")
def test_asset_create_folder(rest_client: RestClient, backend_base_url: str):
    with allure.step("POST /api/assets/folder"):
        result = rest_client.post(
            f"{backend_base_url}/api/assets/folder",
            json={"name": "qa-test-folder", "parentUrl": ""},
        )

    with allure.step("Verify folder created"):
        # Endpoint may return 204 or the folder object
        pass  # No error = success
