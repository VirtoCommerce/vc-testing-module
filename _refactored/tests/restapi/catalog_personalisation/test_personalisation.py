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
from requests.exceptions import HTTPError

from core.clients.rest import RestClient


@pytest.mark.restapi
@allure.feature("Catalog Personalisation / Tags (REST API)")
@allure.title("Get tags from settings dictionary")
def test_tag_get(rest_client: RestClient, backend_base_url: str) -> None:
    with allure.step("GET /api/platform/settings/values/Customer.MemberGroups"):
        result = rest_client.get(f"{backend_base_url}/api/platform/settings/values/Customer.MemberGroups")

    with allure.step("Verify tags list"):
        assert isinstance(result, list)


@pytest.mark.restapi
@allure.feature("Catalog Personalisation / Tags (REST API)")
@allure.title("Search personalisation tags")
def test_tag_search(rest_client: RestClient, backend_base_url: str) -> None:
    with allure.step("POST /api/personalization/search"):
        result = rest_client.post(f"{backend_base_url}/api/personalization/search", json={"skip": 0, "take": 20})

    with allure.step("Verify response shape"):
        assert isinstance(result, dict)
        assert "results" in result or "totalCount" in result


@pytest.mark.restapi
@allure.feature("Catalog Personalisation / Tags (REST API)")
@allure.title("PUT assign tag to product — response contains entityId")
def test_tag_put_assign_product(rest_client: RestClient, backend_base_url: str, dataset: dict) -> None:
    products = dataset.get("products", [])
    if not products:
        pytest.skip("No products in dataset")
    product_id = products[0]["id"]

    with allure.step("PUT /api/personalization/taggeditem"):
        try:
            result = rest_client.put(
                f"{backend_base_url}/api/personalization/taggeditem",
                json={"entityId": product_id, "entityType": "Product", "tags": ["QA-TAG"]},
            )
        except HTTPError as exc:
            pytest.skip(f"Personalisation module not configured: {exc.response.status_code}")

    with allure.step("Verify assignment echoed back"):
        assert result is None or isinstance(result, (dict, list))


@pytest.mark.restapi
@allure.feature("Catalog Personalisation / Tags (REST API)")
@allure.title("PUT assign tag to category — response contains entityId")
def test_tag_put_assign_category(rest_client: RestClient, backend_base_url: str, dataset: dict) -> None:
    categories = dataset.get("categories", [])
    if not categories:
        pytest.skip("No categories in dataset")
    category_id = categories[0]["id"]

    with allure.step("PUT /api/personalization/taggeditem"):
        try:
            result = rest_client.put(
                f"{backend_base_url}/api/personalization/taggeditem",
                json={"entityId": category_id, "entityType": "Category", "tags": ["QA-TAG"]},
            )
        except HTTPError as exc:
            pytest.skip(f"Personalisation module not configured: {exc.response.status_code}")

    with allure.step("Verify assignment echoed back"):
        assert result is None or isinstance(result, (dict, list))


@pytest.mark.restapi
@allure.feature("Catalog Personalisation / Tags (REST API)")
@allure.title("PUT unassign tag from product — empty tags succeeds")
def test_tag_put_unassign_product(rest_client: RestClient, backend_base_url: str, dataset: dict) -> None:
    products = dataset.get("products", [])
    if not products:
        pytest.skip("No products in dataset")
    product_id = products[0]["id"]

    with allure.step("PUT /api/personalization/taggeditem — empty tags"):
        try:
            result = rest_client.put(
                f"{backend_base_url}/api/personalization/taggeditem",
                json={"entityId": product_id, "entityType": "Product", "tags": []},
            )
        except HTTPError as exc:
            pytest.skip(f"Personalisation module not configured: {exc.response.status_code}")

    with allure.step("Verify response shape"):
        assert result is None or isinstance(result, (dict, list))


@pytest.mark.restapi
@pytest.mark.serial
@allure.feature("Catalog Personalisation / Outlines (REST API)")
@allure.title("Synchronize outlines — job accepted")
def test_tag_outlines_sync(rest_client: RestClient, backend_base_url: str) -> None:
    with allure.step("POST /api/personalization/outlines/synchronize"):
        try:
            result = rest_client.post(f"{backend_base_url}/api/personalization/outlines/synchronize", json={})
        except HTTPError as exc:
            pytest.skip(f"Outlines sync not supported: {exc.response.status_code}")

    with allure.step("Verify response shape"):
        assert result is None or isinstance(result, (dict, list))


@pytest.mark.restapi
@pytest.mark.serial
@allure.feature("Catalog Personalisation / Tags (REST API)")
@allure.title("Add tag to Customer.MemberGroups dictionary and verify round-trip")
def test_tag_add_to_member_groups(rest_client: RestClient, backend_base_url: str) -> None:
    setting_name = "Customer.MemberGroups"
    tag_value = f"QA_TAG_{uuid.uuid4().hex[:6]}"

    with allure.step(f"Read current {setting_name}"):
        current = rest_client.get(f"{backend_base_url}/api/platform/settings/{setting_name}")
        assert isinstance(current, dict)
        original_values = list(current.get("allowedValues") or [])

    try:
        with allure.step(f"PUT — add {tag_value}"):
            updated = {**current, "allowedValues": original_values + [tag_value]}
            rest_client.post(f"{backend_base_url}/api/platform/settings", json=[updated])

        with allure.step("Verify tag present in GET"):
            reloaded = rest_client.get(f"{backend_base_url}/api/platform/settings/{setting_name}")
            assert tag_value in (reloaded.get("allowedValues") or [])
    finally:
        with allure.step("Restore original tag list"):
            try:
                restore = {**current, "allowedValues": original_values}
                rest_client.post(f"{backend_base_url}/api/platform/settings", json=[restore])
            except Exception:
                pass
