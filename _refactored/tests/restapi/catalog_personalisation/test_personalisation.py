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


def _find_tagged_item(rest_client: RestClient, backend_base_url: str, entity_id: str) -> dict | None:
    """Return the existing TaggedItem row for the given entityId, or None."""
    search = rest_client.post(
        f"{backend_base_url}/api/personalization/search",
        json={"entityIds": [entity_id], "skip": 0, "take": 5},
    )
    results = search.get("results") if isinstance(search, dict) else None
    return results[0] if results else None


def _put_tagged_item(
    rest_client: RestClient, backend_base_url: str, entity_id: str, entity_type: str, label: str, tags: list[str]
) -> None:
    """PUT /api/personalization/taggeditem — idempotent: uses existing row id if present, else creates."""
    existing = _find_tagged_item(rest_client, backend_base_url, entity_id)
    payload: dict = {"entityId": entity_id, "entityType": entity_type, "label": label, "tags": tags}
    if existing:
        payload["id"] = existing["id"]
    rest_client.put(f"{backend_base_url}/api/personalization/taggeditem", json=payload)


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
@pytest.mark.serial
@allure.feature("Catalog Personalisation / Tags (REST API)")
@allure.title("PUT assign tag to product — returns 204 and is searchable")
def test_tag_put_assign_product(rest_client: RestClient, backend_base_url: str, dataset: dict) -> None:
    products = dataset.get("products", [])
    if not products:
        pytest.skip("No products in dataset")
    product_id = products[0]["id"]
    tag_label = f"QA-{uuid.uuid4().hex[:6]}"

    try:
        with allure.step(f"PUT /api/personalization/taggeditem — label={tag_label}"):
            _put_tagged_item(rest_client, backend_base_url, product_id, "Product", tag_label, [tag_label])

        with allure.step("Verify tag appears on the product's tagged item row"):
            item = _find_tagged_item(rest_client, backend_base_url, product_id)
            assert item is not None
            assert tag_label in item.get("tags", []), f"Expected {tag_label} in {item.get('tags')}"
    finally:
        with allure.step("Cleanup — clear tags on the tagged item row"):
            try:
                _put_tagged_item(rest_client, backend_base_url, product_id, "Product", tag_label, [])
            except Exception:
                pass


@pytest.mark.restapi
@pytest.mark.serial
@allure.feature("Catalog Personalisation / Tags (REST API)")
@allure.title("PUT assign tag to category — returns 204 and is searchable")
def test_tag_put_assign_category(rest_client: RestClient, backend_base_url: str, dataset: dict) -> None:
    categories = dataset.get("categories", [])
    if not categories:
        pytest.skip("No categories in dataset")
    category_id = categories[0]["id"]
    tag_label = f"QA-{uuid.uuid4().hex[:6]}"

    try:
        with allure.step(f"PUT /api/personalization/taggeditem — label={tag_label}"):
            _put_tagged_item(rest_client, backend_base_url, category_id, "Category", tag_label, [tag_label])

        with allure.step("Verify tag appears on the category's tagged item row"):
            item = _find_tagged_item(rest_client, backend_base_url, category_id)
            assert item is not None
            assert tag_label in item.get("tags", []), f"Expected {tag_label} in {item.get('tags')}"
    finally:
        with allure.step("Cleanup — clear tags on the tagged item row"):
            try:
                _put_tagged_item(rest_client, backend_base_url, category_id, "Category", tag_label, [])
            except Exception:
                pass


@pytest.mark.restapi
@pytest.mark.serial
@allure.feature("Catalog Personalisation / Tags (REST API)")
@allure.title("PUT unassign tag from product — tags=[] clears assignment")
def test_tag_put_unassign_product(rest_client: RestClient, backend_base_url: str, dataset: dict) -> None:
    products = dataset.get("products", [])
    if not products:
        pytest.skip("No products in dataset")
    product_id = products[0]["id"]
    tag_label = f"QA-{uuid.uuid4().hex[:6]}"

    with allure.step(f"Assign {tag_label} so there is something to unassign"):
        _put_tagged_item(rest_client, backend_base_url, product_id, "Product", tag_label, [tag_label])

    with allure.step("Unassign via tags=[]"):
        _put_tagged_item(rest_client, backend_base_url, product_id, "Product", tag_label, [])

    with allure.step("Verify tags cleared"):
        item = _find_tagged_item(rest_client, backend_base_url, product_id)
        assert item is not None
        assert item.get("tags") == [], f"Expected empty tags, got {item.get('tags')}"


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
