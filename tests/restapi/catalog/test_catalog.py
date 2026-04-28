"""Catalog CRUD — migrated from Katalon `API Coverage/ModuleCatalog/catalog*`."""

import uuid

import allure
import pytest

from restapi.operations import CatalogOperations, CategoryOperations


@pytest.mark.restapi
@allure.feature("Catalog / Catalogs (REST API)")
@allure.title("Create catalog — physical with default language")
def test_catalog_create(make_catalog) -> None:
    with allure.step("POST /api/catalog/catalogs"):
        catalog = make_catalog()

    with allure.step("Verify response"):
        assert catalog.id, "Catalog id missing"
        assert catalog.name.startswith("QACatalog_")
        assert catalog.is_virtual is False

    with allure.step("Verify default language"):
        assert any(lang.is_default and lang.language_code == "en-US" for lang in catalog.languages)


@pytest.mark.restapi
@allure.feature("Catalog / Catalogs (REST API)")
@allure.title("Create catalog — virtual")
def test_catalog_create_virtual(make_catalog, catalog_ops: CatalogOperations) -> None:
    name = f"QACatalog_Virtual_{uuid.uuid4().hex[:8]}"

    with allure.step(f"POST /api/catalog/catalogs — isVirtual=True, name={name}"):
        catalog = make_catalog(name=name, isVirtual=True)

    with allure.step("Verify virtual catalog"):
        assert catalog.is_virtual is True

    with allure.step("Verify searchable"):
        search = catalog_ops.search(keyword=name)
        found = next((r for r in search.get("results", []) if r["id"] == catalog.id), None)
        assert found is not None
        assert found["isVirtual"] is True


@pytest.mark.restapi
@allure.feature("Catalog / Catalogs (REST API)")
@allure.title("Update catalog — rename")
def test_catalog_update(make_catalog, catalog_ops: CatalogOperations) -> None:
    catalog = make_catalog()
    new_name = f"{catalog.name}_UPD_{uuid.uuid4().hex[:4]}"

    with allure.step(f"PUT /api/catalog/catalogs — rename to {new_name}"):
        catalog_ops.update(catalog, name=new_name)

    with allure.step("Verify rename via search"):
        search = catalog_ops.search(keyword=new_name)
        names = [r["name"] for r in search.get("results", [])]
        assert new_name in names


@pytest.mark.restapi
@allure.feature("Catalog / Catalogs (REST API)")
@allure.title("Search catalog by keyword")
def test_catalog_search(make_catalog, catalog_ops: CatalogOperations) -> None:
    catalog = make_catalog()

    with allure.step(f"POST /api/catalog/catalogs/search keyword={catalog.name}"):
        search = catalog_ops.search(keyword=catalog.name)

    with allure.step("Verify created catalog appears in results"):
        assert search.get("totalCount", 0) >= 1
        found = next((r for r in search.get("results", []) if r["id"] == catalog.id), None)
        assert found is not None


@pytest.mark.restapi
@allure.feature("Catalog / Catalogs (REST API)")
@allure.title("Delete catalog")
def test_catalog_delete(make_catalog, catalog_ops: CatalogOperations) -> None:
    catalog = make_catalog()

    with allure.step(f"DELETE /api/catalog/catalogs/{catalog.id}"):
        catalog_ops.delete(catalog.id)

    with allure.step("Verify catalog no longer in search"):
        search = catalog_ops.search(keyword=catalog.name)
        ids = [r["id"] for r in search.get("results", [])]
        assert catalog.id not in ids


@pytest.mark.restapi
@allure.feature("Catalog / Catalogs (REST API)")
@allure.title("Search listentries within catalog")
def test_catalog_listentries_search(make_product, category_ops: CategoryOperations) -> None:
    product = make_product()

    with allure.step(
        f"POST /api/catalog/listentries — catalogId={product['catalogId']} categoryId={product['categoryId']}"
    ):
        result = category_ops.search(
            catalog_id=product["catalogId"],
            categoryId=product["categoryId"],
            responseGroup="withCategories, withProducts",
            take=200,
        )

    with allure.step("Verify product appears in listentries results"):
        entries = result.get("listEntries") or result.get("results") or []
        ids = [e.get("id") for e in entries]
        assert product["id"] in ids, f"Product {product['id']} not in listentries: {ids}"
