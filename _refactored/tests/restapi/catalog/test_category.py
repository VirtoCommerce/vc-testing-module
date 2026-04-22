"""Category CRUD — migrated from Katalon `API Coverage/ModuleCatalog/category*`."""

import uuid

import allure
import pytest
from requests.exceptions import HTTPError

from restapi.operations import CategoryOperations


@pytest.mark.restapi
@allure.feature("Catalog / Categories (REST API)")
@allure.title("Create category")
def test_category_create(make_category) -> None:
    with allure.step("POST /api/catalog/categories"):
        category = make_category()

    with allure.step("Verify response"):
        assert category["id"], "Category id missing"
        assert category["name"].startswith("QACategory_")
        assert category["catalogId"]


@pytest.mark.restapi
@allure.feature("Catalog / Categories (REST API)")
@allure.title("Update category — rename")
def test_category_update(make_category, category_ops: CategoryOperations) -> None:
    category = make_category()
    new_name = f"{category['name']}_UPD_{uuid.uuid4().hex[:4]}"

    with allure.step(f"POST /api/catalog/categories — rename to {new_name}"):
        category_ops.update(category, name=new_name)

    with allure.step("Verify rename via GET"):
        reloaded = category_ops.get_by_id(category["id"])
        assert reloaded["name"] == new_name


@pytest.mark.restapi
@allure.feature("Catalog / Categories (REST API)")
@allure.title("Get category by id")
def test_category_get_by_id(make_category, category_ops: CategoryOperations) -> None:
    category = make_category()

    with allure.step(f"GET /api/catalog/categories/{category['id']}"):
        reloaded = category_ops.get_by_id(category["id"])

    with allure.step("Verify fields match"):
        assert reloaded["id"] == category["id"]
        assert reloaded["name"] == category["name"]
        assert reloaded["code"] == category["code"]
        assert reloaded["catalogId"] == category["catalogId"]


@pytest.mark.restapi
@allure.feature("Catalog / Categories (REST API)")
@allure.title("Search category — list entries within catalog")
def test_category_search(make_category, category_ops: CategoryOperations) -> None:
    category = make_category()

    with allure.step(f"POST /api/catalog/listentries — catalogId={category['catalogId']}"):
        search = category_ops.search(catalog_id=category["catalogId"])

    with allure.step("Verify created category in results"):
        assert search.get("totalCount", 0) >= 1
        entries = search.get("listEntries", [])
        found = next((e for e in entries if e["id"] == category["id"]), None)
        assert found is not None


@pytest.mark.restapi
@allure.feature("Catalog / Categories (REST API)")
@allure.title("Get new category template for catalog")
def test_category_get_template(make_catalog, category_ops: CategoryOperations) -> None:
    catalog = make_catalog()

    with allure.step(f"GET /api/catalog/{catalog['id']}/categories/newcategory"):
        template = category_ops.get_new_template(catalog["id"])

    with allure.step("Verify template has Category SEO type"):
        assert template.get("seoObjectType") == "Category"


@pytest.mark.restapi
@allure.feature("Catalog / Categories (REST API)")
@allure.title("Create nested subcategory — parentId wired correctly")
def test_category_nested(make_category, category_ops: CategoryOperations) -> None:
    parent = make_category()

    with allure.step(f"POST /api/catalog/categories — child under parent {parent['id']}"):
        child = make_category(
            catalog={"id": parent["catalogId"]},
            parentId=parent["id"],
        )

    with allure.step("Verify child has parentId and shares catalogId"):
        reloaded = category_ops.get_by_id(child["id"])
        assert reloaded["parentId"] == parent["id"]
        assert reloaded["catalogId"] == parent["catalogId"]


@pytest.mark.restapi
@allure.feature("Catalog / Categories (REST API)")
@allure.title("Get category by non-existent id — expect 404")
def test_category_get_not_found(category_ops: CategoryOperations) -> None:
    bogus_id = f"qa-missing-{uuid.uuid4().hex}"

    with allure.step(f"GET /api/catalog/categories/{bogus_id}"):
        with pytest.raises(HTTPError) as exc_info:
            category_ops.get_by_id(bogus_id)
        assert exc_info.value.response.status_code == 404


@pytest.mark.restapi
@allure.feature("Catalog / Categories (REST API)")
@allure.title("Delete category")
def test_category_delete(make_category, category_ops: CategoryOperations) -> None:
    category = make_category()

    with allure.step(f"POST /api/catalog/listentries/delete — objectIds=[{category['id']}]"):
        category_ops.delete(category["id"])

    with allure.step("Verify category no longer returned by GET"):
        try:
            reloaded = category_ops.get_by_id(category["id"])
        except HTTPError as e:
            assert e.response.status_code == 404
        else:
            assert not reloaded or reloaded.get("id") != category["id"]
