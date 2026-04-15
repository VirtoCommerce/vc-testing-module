"""Category CRUD — migrated from Katalon `API Coverage/ModuleCatalog/category*`.

Originals:
- categoryCreate    → test_category_create
- categoryUpdate    → test_category_update
- categoryGetById   → test_category_get_by_id
- categoryDelete    → test_category_delete

Key differences from Katalon:
- Each test gets a fresh implicit catalog via make_category (which composes
  make_catalog). No dependency on `GlobalVariable.catalogId` being populated
  by a prior test run.
- Category DELETE goes through /api/catalog/listentries/delete, not a
  category-specific endpoint — matches the Katalon ListentriesDelete request.
"""

import uuid

import allure
import pytest

from webapi_operations.catalog.category_operations import CategoryOperations


@pytest.mark.webapi
@allure.feature("Catalog / Categories (WebAPI)")
@allure.title("Create category")
def test_category_create(make_category):
    with allure.step("POST /api/catalog/categories"):
        category = make_category()

    assert category["id"], "Category id missing from create response"
    assert category["name"].startswith("QACategory_"), f"Unexpected name: {category['name']}"
    assert category["catalogId"], "catalogId missing from response"


@pytest.mark.webapi
@allure.feature("Catalog / Categories (WebAPI)")
@allure.title("Update category — rename")
def test_category_update(make_category, category_operations: CategoryOperations):
    category = make_category()
    new_name = f"{category['name']}_UPD_{uuid.uuid4().hex[:4]}"

    with allure.step(f"POST /api/catalog/categories — rename to {new_name}"):
        category_operations.update(category, name=new_name)

    with allure.step("Verify rename via GET"):
        reloaded = category_operations.get_by_id(category["id"])
        assert reloaded["name"] == new_name, f"Expected {new_name}, got {reloaded['name']}"


@pytest.mark.webapi
@allure.feature("Catalog / Categories (WebAPI)")
@allure.title("Get category by id")
def test_category_get_by_id(make_category, category_operations: CategoryOperations):
    category = make_category()

    with allure.step(f"GET /api/catalog/categories/{category['id']}"):
        reloaded = category_operations.get_by_id(category["id"])

    assert reloaded["id"] == category["id"]
    assert reloaded["name"] == category["name"]
    assert reloaded["code"] == category["code"]
    assert reloaded["catalogId"] == category["catalogId"]


@pytest.mark.webapi
@allure.feature("Catalog / Categories (WebAPI)")
@allure.title("Delete category")
def test_category_delete(make_category, category_operations: CategoryOperations):
    category = make_category()

    with allure.step(f"POST /api/catalog/listentries/delete — objectIds=[{category['id']}]"):
        category_operations.delete(category["id"])

    with allure.step("Verify category no longer returned by GET"):
        from requests.exceptions import HTTPError

        try:
            reloaded = category_operations.get_by_id(category["id"])
        except HTTPError as e:
            # 404 after delete is the expected path.
            assert e.response.status_code == 404, f"Unexpected status {e.response.status_code}"
        else:
            # Some backends return an empty object instead of 404 — accept either.
            assert (
                not reloaded or reloaded.get("id") != category["id"]
            ), f"Category still returned after delete: {reloaded}"
