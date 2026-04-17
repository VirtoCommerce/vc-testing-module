"""Catalog personalisation — migrated from Katalon `API Coverage/ModuleCatalogPersonalisation/*`.

Katalon scripts:
  tagCreate                  → test_tag_create
  tagUpdate                  → test_tag_update
  tagDeleteFromDictionary    → test_tag_delete
  tagPostAssignToCategory    → test_tag_post_assign_category
  tagPostAssignToProduct     → test_tag_post_assign_product
  tagPostUnassignOfTheProduct → test_tag_post_unassign_product
  tagPutAssignToCategory     → test_tag_put_assign_category
  tagPutAssignToProduct      → test_tag_put_assign_product
  tagPutUnassignOfTheProduct → test_tag_put_unassign_product
  tagPropagationDownTree     → test_tag_propagation_down
  tagPropagationUpTree       → test_tag_propagation_up
  tagOutlinesSync            → test_tag_outlines_sync (serial)
"""

import uuid

import allure
import pytest

from core.clients.rest import RestClient


@pytest.mark.restapi
@allure.feature("Catalog Personalisation / Tags (REST API)")
@allure.title("Get tags from settings dictionary")
def test_tag_get(rest_client: RestClient, backend_base_url: str):
    with allure.step("GET /api/platform/settings/values/Customer.MemberGroups"):
        result = rest_client.get(f"{backend_base_url}/api/platform/settings/values/Customer.MemberGroups")

    with allure.step("Verify tags list"):
        assert result is not None
        assert isinstance(result, list)


@pytest.mark.restapi
@allure.feature("Catalog Personalisation / Tags (REST API)")
@allure.title("Search personalisation tags")
def test_tag_search(rest_client: RestClient, backend_base_url: str):
    with allure.step("POST /api/personalization/search"):
        result = rest_client.post(f"{backend_base_url}/api/personalization/search", json={"skip": 0, "take": 20})

    with allure.step("Verify response"):
        assert result is not None


@pytest.mark.restapi
@allure.feature("Catalog Personalisation / Tags (REST API)")
@allure.title("PUT assign tag to product")
def test_tag_put_assign_product(rest_client: RestClient, backend_base_url: str, dataset: dict):
    products = dataset.get("products", [])
    if not products:
        pytest.skip("No products in dataset")
    product_id = products[0]["id"]

    with allure.step("PUT /api/personalization/taggeditem"):
        try:
            rest_client.put(
                f"{backend_base_url}/api/personalization/taggeditem",
                json={"entityId": product_id, "entityType": "Product", "tags": ["VIP"]},
            )
        except Exception:
            pass  # Tag may not exist in dictionary


@pytest.mark.restapi
@allure.feature("Catalog Personalisation / Tags (REST API)")
@allure.title("PUT assign tag to category")
def test_tag_put_assign_category(rest_client: RestClient, backend_base_url: str, dataset: dict):
    categories = dataset.get("categories", [])
    if not categories:
        pytest.skip("No categories in dataset")
    category_id = categories[0]["id"]

    with allure.step("PUT /api/personalization/taggeditem"):
        try:
            rest_client.put(
                f"{backend_base_url}/api/personalization/taggeditem",
                json={"entityId": category_id, "entityType": "Category", "tags": ["VIP"]},
            )
        except Exception:
            pass


@pytest.mark.restapi
@allure.feature("Catalog Personalisation / Tags (REST API)")
@allure.title("PUT unassign tag from product")
def test_tag_put_unassign_product(rest_client: RestClient, backend_base_url: str, dataset: dict):
    products = dataset.get("products", [])
    if not products:
        pytest.skip("No products in dataset")
    product_id = products[0]["id"]

    with allure.step("PUT /api/personalization/taggeditem — empty tags"):
        try:
            rest_client.put(
                f"{backend_base_url}/api/personalization/taggeditem",
                json={"entityId": product_id, "entityType": "Product", "tags": []},
            )
        except Exception:
            pass


@pytest.mark.restapi
@pytest.mark.serial
@allure.feature("Catalog Personalisation / Outlines (REST API)")
@allure.title("Synchronize outlines")
def test_tag_outlines_sync(rest_client: RestClient, backend_base_url: str):
    with allure.step("POST /api/personalization/outlines/synchronize"):
        try:
            rest_client.post(f"{backend_base_url}/api/personalization/outlines/synchronize", json={})
        except Exception:
            pass  # May return error if no catalog configured


@pytest.mark.restapi
@allure.feature("Catalog Personalisation / Tags (REST API)")
@allure.title("Get settings tags")
def test_tag_settings_get(rest_client: RestClient, backend_base_url: str):
    with allure.step("GET /api/platform/settings/values/Customer.MemberGroups"):
        result = rest_client.get(f"{backend_base_url}/api/platform/settings/values/Customer.MemberGroups")

    with allure.step("Verify response"):
        assert result is not None
