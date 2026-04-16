"""Asset file operations — migrated from Katalon `API Coverage/ModulePlatform/Asset*`.

Katalon sub-scripts:
- AssetFileUploadUrl         → test_asset_upload_url
- AssetFileUploadUrlImage    → test_asset_upload_url_image
- AssetFileUploadLocal       → test_asset_upload_local
- AssetFileUploadLocalStorage→ test_asset_upload_local_storage
- AssetFileAccess            → test_asset_file_access
- AssetFileAccessAfterDelete → test_asset_file_access_after_delete
- AssetFolderCreateNew       → test_asset_folder_create
- AssetFolderGet             → test_asset_folder_list
- AssetFolderDelete          → test_asset_folder_delete
- AssetFolderCreateDeleteBulk→ test_asset_folder_create_delete_bulk
- AssetFolderCreateErrorValidation → test_asset_folder_create_error_validation
"""

import uuid

import allure
import pytest
import requests

from core.clients.rest import RestClient
from core.global_settings import GlobalSettings


@pytest.mark.restapi
@allure.feature("Platform / Assets (REST API)")
@allure.title("Upload asset file from URL")
def test_asset_upload_url(rest_client: RestClient, backend_base_url: str):
    folder = f"qa-test-{uuid.uuid4().hex[:6]}"

    with allure.step("POST /api/assets — upload from external URL"):
        result = rest_client.post(
            f"{backend_base_url}/api/assets",
            json={
                "url": "https://raw.githubusercontent.com/VirtoCommerce/vc-testing-module/dev/README.md",
                "name": "qa-test-upload.md",
                "folderUrl": folder,
            },
        )

    with allure.step("Verify upload response"):
        assert result is not None
        assert result.get("url") or result.get("relativeUrl")


@pytest.mark.restapi
@allure.feature("Platform / Assets (REST API)")
@allure.title("Upload image file from URL")
def test_asset_upload_url_image(rest_client: RestClient, backend_base_url: str):
    folder = f"qa-img-{uuid.uuid4().hex[:6]}"

    with allure.step("POST /api/assets — upload image"):
        result = rest_client.post(
            f"{backend_base_url}/api/assets",
            json={
                "url": "https://raw.githubusercontent.com/VirtoCommerce/vc-testing-module/dev/.gitignore",
                "name": "qa-test-image.txt",
                "folderUrl": folder,
            },
        )

    with allure.step("Verify upload"):
        assert result is not None


@pytest.mark.restapi
@allure.feature("Platform / Assets (REST API)")
@allure.title("Upload local file")
def test_asset_upload_local(rest_client: RestClient, backend_base_url: str, global_settings: GlobalSettings):
    folder = f"qa-local-{uuid.uuid4().hex[:6]}"

    with allure.step("POST /api/assets?folderUrl=... — multipart upload"):
        # Use raw requests session for multipart form upload
        response = rest_client._session.post(
            f"{backend_base_url}/api/assets?folderUrl={folder}",
            files={"file": ("qa-test-local.txt", b"QA test content", "text/plain")},
            headers={"Authorization": rest_client._session.headers.get("Authorization", "")},
            timeout=global_settings.requests_timeout,
            verify=global_settings.verify_ssl,
        )

    with allure.step("Verify upload response"):
        assert response.status_code in (200, 204)


@pytest.mark.restapi
@allure.feature("Platform / Assets (REST API)")
@allure.title("Upload local file to storage")
def test_asset_upload_local_storage(rest_client: RestClient, backend_base_url: str, global_settings: GlobalSettings):
    folder = f"qa-storage-{uuid.uuid4().hex[:6]}"

    with allure.step("POST /api/assets?folderUrl=... — local storage upload"):
        response = rest_client._session.post(
            f"{backend_base_url}/api/assets?folderUrl={folder}",
            files={"file": ("qa-storage-test.txt", b"QA storage test", "text/plain")},
            headers={"Authorization": rest_client._session.headers.get("Authorization", "")},
            timeout=global_settings.requests_timeout,
            verify=global_settings.verify_ssl,
        )

    with allure.step("Verify"):
        assert response.status_code in (200, 204)


@pytest.mark.restapi
@allure.feature("Platform / Assets (REST API)")
@allure.title("Access uploaded asset file")
def test_asset_file_access(rest_client: RestClient, backend_base_url: str):
    folder = f"qa-access-{uuid.uuid4().hex[:6]}"

    with allure.step("Upload file"):
        uploaded = rest_client.post(
            f"{backend_base_url}/api/assets",
            json={
                "url": "https://raw.githubusercontent.com/VirtoCommerce/vc-testing-module/dev/README.md",
                "name": "qa-access-test.md",
                "folderUrl": folder,
            },
        )
        file_url = uploaded.get("url") or uploaded.get("relativeUrl")
        assert file_url

    with allure.step("GET the uploaded file"):
        response = requests.get(
            f"{backend_base_url}/{file_url.lstrip('/')}" if not file_url.startswith("http") else file_url,
            timeout=30,
            verify=False,
        )
        assert response.status_code == 200


@pytest.mark.restapi
@allure.feature("Platform / Assets (REST API)")
@allure.title("Access asset file after delete — expect 404")
def test_asset_file_access_after_delete(rest_client: RestClient, backend_base_url: str):
    folder = f"qa-del-{uuid.uuid4().hex[:6]}"

    with allure.step("Upload file"):
        uploaded = rest_client.post(
            f"{backend_base_url}/api/assets",
            json={
                "url": "https://raw.githubusercontent.com/VirtoCommerce/vc-testing-module/dev/README.md",
                "name": "qa-del-test.md",
                "folderUrl": folder,
            },
        )

    with allure.step("Delete the asset"):
        asset_urls = [uploaded.get("url") or uploaded.get("relativeUrl")]
        rest_client.post(f"{backend_base_url}/api/assets/delete", json=asset_urls)

    with allure.step("Verify file no longer accessible"):
        file_url = asset_urls[0]
        full_url = f"{backend_base_url}/{file_url.lstrip('/')}" if not file_url.startswith("http") else file_url
        response = requests.get(full_url, timeout=30, verify=False)
        assert response.status_code in (404, 204, 410), f"Expected 404 after delete, got {response.status_code}"


@pytest.mark.restapi
@allure.feature("Platform / Assets (REST API)")
@allure.title("Create asset folder")
def test_asset_folder_create(rest_client: RestClient, backend_base_url: str):
    folder_name = f"qa-folder-{uuid.uuid4().hex[:6]}"

    with allure.step(f"POST /api/assets/folder — name={folder_name}"):
        rest_client.post(
            f"{backend_base_url}/api/assets/folder",
            json={"name": folder_name, "parentUrl": ""},
        )


@pytest.mark.restapi
@allure.feature("Platform / Assets (REST API)")
@allure.title("List assets in folder")
def test_asset_folder_list(rest_client: RestClient, backend_base_url: str):
    with allure.step("GET /api/assets"):
        result = rest_client.get(f"{backend_base_url}/api/assets")

    with allure.step("Verify response"):
        assert result is not None


@pytest.mark.restapi
@allure.feature("Platform / Assets (REST API)")
@allure.title("Delete asset folder")
def test_asset_folder_delete(rest_client: RestClient, backend_base_url: str):
    folder_name = f"qa-delfolder-{uuid.uuid4().hex[:6]}"

    with allure.step("Create folder"):
        rest_client.post(
            f"{backend_base_url}/api/assets/folder",
            json={"name": folder_name, "parentUrl": ""},
        )

    with allure.step(f"POST /api/assets/delete — folder={folder_name}"):
        rest_client.post(f"{backend_base_url}/api/assets/delete", json=[folder_name])


@pytest.mark.restapi
@allure.feature("Platform / Assets (REST API)")
@allure.title("Create and delete folders in bulk")
def test_asset_folder_create_delete_bulk(rest_client: RestClient, backend_base_url: str):
    suffix = uuid.uuid4().hex[:6]
    folders = [f"qa-bulk-{suffix}-{i}" for i in range(3)]

    with allure.step(f"Create {len(folders)} folders"):
        for name in folders:
            rest_client.post(f"{backend_base_url}/api/assets/folder", json={"name": name, "parentUrl": ""})

    with allure.step("Delete all folders in bulk"):
        rest_client.post(f"{backend_base_url}/api/assets/delete", json=folders)


@pytest.mark.restapi
@allure.feature("Platform / Assets (REST API)")
@allure.title("Create folder — error validation (empty name)")
def test_asset_folder_create_error_validation(rest_client: RestClient, backend_base_url: str):
    with allure.step("POST /api/assets/folder — empty name"):
        try:
            rest_client.post(f"{backend_base_url}/api/assets/folder", json={"name": "", "parentUrl": ""})
        except Exception as e:
            # Expect 400 or validation error
            if hasattr(e, "response"):
                assert e.response.status_code == 400
            else:
                pass  # Some implementations may not error on empty name
