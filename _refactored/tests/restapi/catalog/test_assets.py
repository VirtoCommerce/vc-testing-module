"""Asset operations in catalog/product context — migrated from Katalon `API Coverage/ModuleCatalog/asset*`.

Endpoints (verified from Object Repository `.rs` files):
  - POST   /api/assets/folder
  - POST   /api/assets?folderUrl={folder}&url={sourceUrl}   (upload from URL)
  - POST   /api/assets?folderUrl={folder}                    (upload local file, multipart)
  - GET    /api/assets?folderUrl={folder}&keyword={kw}       (list)
  - DELETE /api/assets?urls={url}                            (delete)
"""

import uuid

import allure
import pytest

from core.clients.rest import RestClient
from restapi.operations import ProductOperations


@pytest.mark.restapi
@allure.feature("Catalog / Assets (REST API)")
@allure.title("Create asset blob folder")
def test_asset_create_blob_folder(rest_client: RestClient, backend_base_url: str):
    folder_name = f"qa-cat-folder-{uuid.uuid4().hex[:6]}"

    with allure.step(f"POST /api/assets/folder — {folder_name}"):
        rest_client.post(
            f"{backend_base_url}/api/assets/folder",
            json={"name": folder_name, "parentUrl": ""},
        )

    with allure.step("GET /api/assets — verify folder listed"):
        listing = rest_client.get(f"{backend_base_url}/api/assets", params={"folderUrl": ""})
        results = listing.get("results", []) if isinstance(listing, dict) else (listing or [])
        names = [item.get("name") for item in results]
        assert folder_name in names


@pytest.mark.restapi
@allure.feature("Catalog / Assets (REST API)")
@allure.title("Upload asset file from URL into product folder")
def test_asset_file_upload(rest_client: RestClient, backend_base_url: str):
    folder = f"catalog-{uuid.uuid4().hex[:6]}"
    source_url = "https://raw.githubusercontent.com/VirtoCommerce/vc-testing-module/dev/README.md"

    with allure.step(f"POST /api/assets?folderUrl={folder}&url=..."):
        result = rest_client.post(
            f"{backend_base_url}/api/assets",
            json=None,
            params={"folderUrl": folder, "url": source_url},
        )

    with allure.step("Verify upload response"):
        assert result is not None


@pytest.mark.restapi
@allure.feature("Catalog / Assets (REST API)")
@allure.title("Get assets list in folder")
def test_asset_get_list(rest_client: RestClient, backend_base_url: str):
    with allure.step("GET /api/assets"):
        listing = rest_client.get(f"{backend_base_url}/api/assets", params={"folderUrl": ""})

    with allure.step("Verify list response"):
        results = listing.get("results", []) if isinstance(listing, dict) else (listing or [])
        assert isinstance(results, list)


@pytest.mark.restapi
@allure.feature("Catalog / Assets (REST API)")
@allure.title("Add asset to product")
def test_asset_add_to_product(
    make_product,
    product_ops: ProductOperations,
    rest_client: RestClient,
    backend_base_url: str,
):
    product = make_product()
    folder = f"catalog-{product['code']}"
    asset_url = ""

    with allure.step(f"POST /api/assets?folderUrl={folder} — multipart upload"):
        uploaded = rest_client.post_multipart(
            f"{backend_base_url}/api/assets",
            params={"folderUrl": folder},
            files={"file": (f"qa-{uuid.uuid4().hex[:6]}.txt", b"QA asset content", "text/plain")},
        )
        assert uploaded, "Asset upload response empty"
        asset_info = uploaded[0] if isinstance(uploaded, list) else uploaded
        asset_url = asset_info.get("url") or asset_info.get("relativeUrl") or ""

    try:
        with allure.step("POST /api/catalog/products — attach asset via product update"):
            asset_entry = {
                "name": asset_info.get("name"),
                "url": asset_info.get("url"),
                "relativeUrl": asset_info.get("relativeUrl"),
                "mimeType": asset_info.get("contentType") or asset_info.get("mimeType"),
                "size": asset_info.get("size", 0),
                "group": "default",
                "createdDate": "0001-01-01T00:00:00Z",
            }
            product_ops.update(product, assets=[asset_entry])

        with allure.step("Verify asset attached to product"):
            reloaded = product_ops.get_by_id(product["id"])
            asset_names = [a.get("name") for a in reloaded.get("assets", [])]
            assert asset_info.get("name") in asset_names
    finally:
        with allure.step("Cleanup uploaded asset and folder"):
            try:
                if asset_url:
                    rest_client.delete(f"{backend_base_url}/api/assets", params={"urls": [asset_url]})
                rest_client.delete(f"{backend_base_url}/api/assets", params={"urls": [folder]})
            except Exception:
                pass


@pytest.mark.restapi
@allure.feature("Catalog / Assets (REST API)")
@allure.title("Remove asset from product")
def test_asset_remove_from_product(make_product, product_ops: ProductOperations):
    asset_entry = {
        "name": "qa-stub.txt",
        "url": "/qa-stub/qa-stub.txt",
        "relativeUrl": "/qa-stub/qa-stub.txt",
        "mimeType": "text/plain",
        "size": 16,
        "group": "default",
        "createdDate": "0001-01-01T00:00:00Z",
    }
    product = make_product(assets=[asset_entry])

    with allure.step("Verify setup — product has one asset"):
        reloaded = product_ops.get_by_id(product["id"])
        assert len(reloaded.get("assets", [])) == 1

    with allure.step("POST /api/catalog/products — clear assets"):
        product_ops.update(product, assets=[])

    with allure.step("Verify asset removed"):
        reloaded = product_ops.get_by_id(product["id"])
        assert reloaded.get("assets") in ([], None)


@pytest.mark.restapi
@allure.feature("Catalog / Assets (REST API)")
@allure.title("Delete uploaded asset from folder")
def test_asset_delete(rest_client: RestClient, backend_base_url: str):
    folder = f"qa-catdel-{uuid.uuid4().hex[:6]}"
    source_url = "https://raw.githubusercontent.com/VirtoCommerce/vc-testing-module/dev/README.md"

    with allure.step(f"POST /api/assets?folderUrl={folder}&url=... — upload"):
        uploaded = rest_client.post(
            f"{backend_base_url}/api/assets",
            json=None,
            params={"folderUrl": folder, "url": source_url},
        )
        assert uploaded, "Asset upload response empty"
        entry = uploaded[0] if isinstance(uploaded, list) else uploaded
        asset_url = entry.get("url") or entry.get("relativeUrl") or ""
        assert asset_url, "Uploaded asset url missing"

    with allure.step("DELETE /api/assets?urls=..."):
        rest_client.delete(f"{backend_base_url}/api/assets", params={"urls": [asset_url]})

    with allure.step("Verify asset gone from listing"):
        listing = rest_client.get(f"{backend_base_url}/api/assets", params={"folderUrl": folder})
        results = listing.get("results", []) if isinstance(listing, dict) else (listing or [])
        names = [item.get("name") for item in results]
        assert entry.get("name") not in names

    with allure.step("Cleanup folder"):
        try:
            rest_client.delete(f"{backend_base_url}/api/assets", params={"urls": [folder]})
        except Exception:
            pass
