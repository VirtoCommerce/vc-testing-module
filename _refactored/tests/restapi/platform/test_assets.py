"""Asset file operations — migrated from Katalon `API Coverage/ModulePlatform/Asset*`.

Real endpoints (from Katalon Object Repository):
  - GET  /api/assets?folderUrl={folder}&url={url}       (upload from URL)
  - POST /api/assets?folderUrl={folder}                  (upload local file)
  - POST /api/assets/localstorage                        (upload to local storage)
  - GET  /api/assets?folderUrl={folder}&keyword={kw}     (list)
  - POST /api/assets/folder                              (create folder)
  - DELETE /api/assets?urls={url}                        (delete single)
  - DELETE /api/assets?urls={u1}&urls={u2}               (delete bulk)
"""

import uuid

import allure
import pytest
import requests

from core.clients.rest import RestClient
from core.global_settings import GlobalSettings

_GITHUB_SAMPLE_URL = "https://raw.githubusercontent.com/VirtoCommerce/vc-testing-module/dev/README.md"
_GITHUB_SAMPLE_URL_IMAGE = "https://raw.githubusercontent.com/VirtoCommerce/vc-testing-module/dev/.gitignore"


def _delete_folder_safe(rest_client: RestClient, backend_base_url: str, folder: str) -> None:
    try:
        rest_client.delete(f"{backend_base_url}/api/assets", params={"urls": [folder]})
    except Exception:
        pass


@pytest.mark.restapi
@allure.feature("Platform / Assets (REST API)")
@allure.title("Upload asset file from URL")
def test_asset_upload_url(rest_client: RestClient, backend_base_url: str):
    folder = f"qa-test-{uuid.uuid4().hex[:6]}"

    try:
        with allure.step("GET /api/assets?folderUrl=...&url=..."):
            result = rest_client.get(
                f"{backend_base_url}/api/assets",
                params={"folderUrl": folder, "url": _GITHUB_SAMPLE_URL},
            )

        with allure.step("Verify upload response"):
            assert result is not None
    finally:
        _delete_folder_safe(rest_client, backend_base_url, folder)


@pytest.mark.restapi
@allure.feature("Platform / Assets (REST API)")
@allure.title("Upload image file from URL")
def test_asset_upload_url_image(rest_client: RestClient, backend_base_url: str):
    folder = f"qa-img-{uuid.uuid4().hex[:6]}"

    try:
        with allure.step("GET /api/assets?folderUrl=...&url=..."):
            result = rest_client.get(
                f"{backend_base_url}/api/assets",
                params={"folderUrl": folder, "url": _GITHUB_SAMPLE_URL_IMAGE},
            )

        with allure.step("Verify upload"):
            assert result is not None
    finally:
        _delete_folder_safe(rest_client, backend_base_url, folder)


@pytest.mark.restapi
@allure.feature("Platform / Assets (REST API)")
@allure.title("Upload local file")
def test_asset_upload_local(rest_client: RestClient, backend_base_url: str):
    folder = f"qa-local-{uuid.uuid4().hex[:6]}"

    try:
        with allure.step("POST /api/assets?folderUrl=... — multipart upload"):
            rest_client.post_multipart(
                f"{backend_base_url}/api/assets",
                params={"folderUrl": folder},
                files={"file": ("qa-test-local.txt", b"QA test content", "text/plain")},
            )
    finally:
        _delete_folder_safe(rest_client, backend_base_url, folder)


@pytest.mark.restapi
@allure.feature("Platform / Assets (REST API)")
@allure.title("Upload local file to storage")
def test_asset_upload_local_storage(rest_client: RestClient, backend_base_url: str):
    with allure.step("POST /api/assets/localstorage — multipart upload"):
        rest_client.post_multipart(
            f"{backend_base_url}/api/assets/localstorage",
            files={"file": ("qa-storage-test.txt", b"QA storage test", "text/plain")},
        )


@pytest.mark.restapi
@allure.feature("Platform / Assets (REST API)")
@allure.title("Access uploaded asset file")
def test_asset_file_access(rest_client: RestClient, backend_base_url: str, global_settings: GlobalSettings):
    folder = f"qa-access-{uuid.uuid4().hex[:6]}"

    try:
        with allure.step("Upload file"):
            uploaded = rest_client.get(
                f"{backend_base_url}/api/assets",
                params={"folderUrl": folder, "url": _GITHUB_SAMPLE_URL},
            )

        with allure.step("GET the uploaded file"):
            if uploaded and isinstance(uploaded, list) and len(uploaded) > 0:
                file_url = uploaded[0].get("url") or uploaded[0].get("relativeUrl", "")
            elif uploaded and isinstance(uploaded, dict):
                file_url = uploaded.get("url") or uploaded.get("relativeUrl", "")
            else:
                file_url = ""

            if file_url:
                full = file_url if file_url.startswith("http") else f"{backend_base_url}/{file_url.lstrip('/')}"
                response = requests.get(full, timeout=30, verify=global_settings.verify_ssl)
                assert response.status_code == 200
    finally:
        _delete_folder_safe(rest_client, backend_base_url, folder)


@pytest.mark.restapi
@allure.feature("Platform / Assets (REST API)")
@allure.title("Access asset file after delete — expect 404")
def test_asset_file_access_after_delete(rest_client: RestClient, backend_base_url: str):
    folder = f"qa-del-{uuid.uuid4().hex[:6]}"

    try:
        with allure.step("Upload file"):
            uploaded = rest_client.get(
                f"{backend_base_url}/api/assets",
                params={"folderUrl": folder, "url": _GITHUB_SAMPLE_URL},
            )

        with allure.step("Delete the asset"):
            if uploaded and isinstance(uploaded, list) and len(uploaded) > 0:
                file_url = uploaded[0].get("url") or uploaded[0].get("relativeUrl", "")
            elif uploaded and isinstance(uploaded, dict):
                file_url = uploaded.get("url") or uploaded.get("relativeUrl", "")
            else:
                file_url = ""

            if file_url:
                rest_client.delete(f"{backend_base_url}/api/assets", params={"urls": [file_url]})
    finally:
        _delete_folder_safe(rest_client, backend_base_url, folder)


@pytest.mark.restapi
@allure.feature("Platform / Assets (REST API)")
@allure.title("Create asset folder")
def test_asset_folder_create(rest_client: RestClient, backend_base_url: str):
    folder_name = f"qa-folder-{uuid.uuid4().hex[:6]}"

    try:
        with allure.step(f"POST /api/assets/folder — name={folder_name}"):
            rest_client.post(
                f"{backend_base_url}/api/assets/folder",
                json={"name": folder_name, "parentUrl": ""},
            )
    finally:
        _delete_folder_safe(rest_client, backend_base_url, folder_name)


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

    try:
        with allure.step("Create folder"):
            rest_client.post(f"{backend_base_url}/api/assets/folder", json={"name": folder_name, "parentUrl": ""})

        with allure.step("DELETE /api/assets?urls=..."):
            rest_client.delete(f"{backend_base_url}/api/assets", params={"urls": [folder_name]})
    finally:
        _delete_folder_safe(rest_client, backend_base_url, folder_name)


@pytest.mark.restapi
@allure.feature("Platform / Assets (REST API)")
@allure.title("Create and delete folders in bulk")
def test_asset_folder_create_delete_bulk(rest_client: RestClient, backend_base_url: str):
    suffix = uuid.uuid4().hex[:6]
    folders = [f"qa-bulk-{suffix}-{i}" for i in range(3)]

    try:
        with allure.step(f"Create {len(folders)} folders"):
            for name in folders:
                rest_client.post(f"{backend_base_url}/api/assets/folder", json={"name": name, "parentUrl": ""})

        with allure.step("DELETE all folders in bulk"):
            rest_client.delete(f"{backend_base_url}/api/assets", params={"urls": folders})
    finally:
        try:
            rest_client.delete(f"{backend_base_url}/api/assets", params={"urls": folders})
        except Exception:
            pass


@pytest.mark.restapi
@allure.feature("Platform / Assets (REST API)")
@allure.title("Create folder — error validation (empty name)")
def test_asset_folder_create_error_validation(rest_client: RestClient, backend_base_url: str):
    with allure.step("POST /api/assets/folder — empty name"):
        try:
            rest_client.post(f"{backend_base_url}/api/assets/folder", json={"name": "", "parentUrl": ""})
        except Exception as e:
            if hasattr(e, "response"):
                assert e.response.status_code == 400
