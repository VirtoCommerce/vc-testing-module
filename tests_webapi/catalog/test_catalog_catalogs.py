"""Catalog CRUD — pilot migration from Katalon `API Coverage/ModuleCatalog`.

Originals:
- catalogCreate   → test_catalog_create
- catalogUpdate   → test_catalog_update
- catalogSearch   → test_catalog_search
- catalogDelete   → test_catalog_delete

Differences vs. Katalon:
- No GlobalVariable — each test creates its own catalog via `make_catalog`,
  cleaned up in teardown.
- Unique names via uuid suffix (parallel-safe under pytest-xdist).
- Assertions via plain `assert` instead of `WS.verifyElementPropertyValue`.
- Auth via Bearer token (password grant) instead of the `api_key` header.
"""

import uuid

import allure
import pytest

from webapi_operations.catalog.catalog_operations import CatalogOperations


@pytest.mark.webapi
@allure.feature("Catalog / Catalogs (WebAPI)")
@allure.title("Create catalog — physical with default language")
def test_catalog_create(make_catalog):
    with allure.step("POST /api/catalog/catalogs"):
        catalog = make_catalog()

    with allure.step("Verify response contains expected fields"):
        assert catalog["id"], "Catalog id missing from create response"
        assert catalog["name"].startswith("QACatalog_"), f"Unexpected name: {catalog['name']}"
        assert catalog["isVirtual"] is False, f"Expected isVirtual=False, got {catalog['isVirtual']}"

    with allure.step("Verify default language is set"):
        languages = catalog.get("languages", [])
        assert len(languages) >= 1, f"Expected at least 1 language, got {len(languages)}"
        default_langs = [lang for lang in languages if lang.get("isDefault")]
        assert len(default_langs) == 1, f"Expected exactly 1 default language, got {len(default_langs)}"
        assert (
            default_langs[0]["languageCode"] == "en-US"
        ), f"Expected default language 'en-US', got '{default_langs[0]['languageCode']}'"


@pytest.mark.webapi
@allure.feature("Catalog / Catalogs (WebAPI)")
@allure.title("Create catalog — virtual")
def test_catalog_create_virtual(make_catalog, catalog_operations: CatalogOperations):
    custom_name = f"QACatalog_Virtual_{uuid.uuid4().hex[:8]}"

    with allure.step(f"POST /api/catalog/catalogs — isVirtual=True, name={custom_name}"):
        catalog = make_catalog(name=custom_name, isVirtual=True)

    with allure.step("Verify virtual catalog response"):
        assert catalog["id"], "Catalog id missing from create response"
        assert catalog["name"] == custom_name, f"Expected name '{custom_name}', got '{catalog['name']}'"
        assert catalog["isVirtual"] is True, f"Expected isVirtual=True, got {catalog['isVirtual']}"

    with allure.step("Verify virtual catalog is searchable"):
        search = catalog_operations.search(keyword=custom_name)
        found = next((r for r in search.get("results", []) if r["id"] == catalog["id"]), None)
        assert found is not None, f"Virtual catalog {catalog['id']} not found in search results"
        assert found["isVirtual"] is True, "Search result isVirtual should be True"


@pytest.mark.webapi
@allure.feature("Catalog / Catalogs (WebAPI)")
@allure.title("Create catalog — with custom name")
def test_catalog_create_with_custom_name(make_catalog):
    custom_name = f"QACatalog_Custom_{uuid.uuid4().hex[:8]}"

    with allure.step(f"POST /api/catalog/catalogs — name={custom_name}"):
        catalog = make_catalog(name=custom_name)

    assert catalog["id"], "Catalog id missing from create response"
    assert catalog["name"] == custom_name, f"Expected exact name '{custom_name}', got '{catalog['name']}'"


@pytest.mark.webapi
@allure.feature("Catalog / Catalogs (WebAPI)")
@allure.title("Update catalog — rename")
def test_catalog_update(make_catalog, catalog_operations: CatalogOperations):
    catalog = make_catalog()
    new_name = f"{catalog['name']}_UPD_{uuid.uuid4().hex[:4]}"

    with allure.step(f"PUT /api/catalog/catalogs — rename to {new_name}"):
        catalog_operations.update(catalog, name=new_name)

    with allure.step("Verify rename via search"):
        search = catalog_operations.search(keyword=new_name)
        names = [r["name"] for r in search.get("results", [])]
        assert new_name in names, f"Updated name '{new_name}' not found in search. Got: {names}"


@pytest.mark.webapi
@allure.feature("Catalog / Catalogs (WebAPI)")
@allure.title("Search catalog by keyword")
def test_catalog_search(make_catalog, catalog_operations: CatalogOperations):
    catalog = make_catalog()

    with allure.step(f"POST /api/catalog/catalogs/search keyword={catalog['name']}"):
        search = catalog_operations.search(keyword=catalog["name"])

    assert search.get("totalCount", 0) >= 1, "Expected at least one result"
    results = search.get("results", [])
    found = next((r for r in results if r["id"] == catalog["id"]), None)
    assert found is not None, f"Created catalog {catalog['id']} not in search results"
    assert found["name"] == catalog["name"]


@pytest.mark.webapi
@allure.feature("Catalog / Catalogs (WebAPI)")
@allure.title("Delete catalog")
def test_catalog_delete(make_catalog, catalog_operations: CatalogOperations):
    catalog = make_catalog()

    with allure.step(f"DELETE /api/catalog/catalogs/{catalog['id']}"):
        catalog_operations.delete(catalog["id"])

    with allure.step("Verify catalog no longer appears in search"):
        search = catalog_operations.search(keyword=catalog["name"])
        ids = [r["id"] for r in search.get("results", [])]
        assert catalog["id"] not in ids, "Catalog still present after DELETE"

    # Factory teardown will attempt to delete this catalog again and silently
    # swallow the error — no manual removal from the cleanup list is needed.
