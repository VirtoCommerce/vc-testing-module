"""Orders module — migrated from Katalon `API Coverage/ModuleOrders/*`.

Katalon scripts:
  OrderCreate → test_order_create
"""

import uuid
from collections.abc import Generator

import allure
import pytest
from requests.exceptions import HTTPError

from core.clients.rest import RestClient
from core.global_settings import GlobalSettings


@pytest.fixture
def make_order(
    rest_client: RestClient, backend_base_url: str, global_settings: GlobalSettings, dataset: dict
) -> Generator[callable, None, None]:
    """Factory: create a customer order; deletes all created orders at teardown."""
    created_ids: list[str] = []

    def _make(**overrides: dict) -> dict:
        users = dataset.get("users", [])
        customer_id = users[0]["id"] if users else "unknown-user"
        customer_name = users[0].get("userName", "QA User") if users else "QA User"
        payload = {
            "number": f"QA-{uuid.uuid4().hex[:8].upper()}",
            "storeId": global_settings.store_id,
            "customerId": customer_id,
            "customerName": customer_name,
            "currency": "USD",
            "status": "New",
            "items": [],
        }
        payload.update(overrides)
        order = rest_client.post(f"{backend_base_url}/api/order/customerOrders", json=payload)
        created_ids.append(order["id"])
        return order

    yield _make

    for oid in reversed(created_ids):
        try:
            rest_client.delete(f"{backend_base_url}/api/order/customerOrders", params={"ids": [oid]})
        except Exception:
            pass


@pytest.mark.restapi
@allure.feature("Orders (REST API)")
@allure.title("Create order")
def test_order_create(make_order) -> None:
    with allure.step("POST /api/order/customerOrders"):
        order = make_order()

    with allure.step("Verify response"):
        assert order["id"]
        assert order["number"].startswith("QA-")
        assert order["status"] == "New"


@pytest.mark.restapi
@allure.feature("Orders (REST API)")
@allure.title("Search orders")
def test_order_search(rest_client: RestClient, backend_base_url: str) -> None:
    with allure.step("POST /api/order/customerOrders/search"):
        result = rest_client.post(
            f"{backend_base_url}/api/order/customerOrders/search",
            json={"skip": 0, "take": 5},
        )

    with allure.step("Verify"):
        assert result is not None


@pytest.mark.restapi
@allure.feature("Orders (REST API)")
@allure.title("Check indexed search enabled")
def test_order_indexed_search_enabled(rest_client: RestClient, backend_base_url: str) -> None:
    with allure.step("GET /api/order/customerOrders/indexed/searchEnabled"):
        result = rest_client.get(f"{backend_base_url}/api/order/customerOrders/indexed/searchEnabled")

    with allure.step("Verify"):
        assert result is not None


@pytest.mark.restapi
@allure.feature("Orders (REST API)")
@allure.title("Get order by id")
def test_order_get_by_id(make_order, rest_client: RestClient, backend_base_url: str) -> None:
    order = make_order()

    with allure.step(f"GET /api/order/customerOrders/{order['id']}"):
        reloaded = rest_client.get(f"{backend_base_url}/api/order/customerOrders/{order['id']}")

    with allure.step("Verify fields match"):
        assert reloaded["id"] == order["id"]
        assert reloaded["number"] == order["number"]
        assert reloaded["storeId"] == order["storeId"]


@pytest.mark.restapi
@allure.feature("Orders (REST API)")
@allure.title("Update order status")
def test_order_update_status(make_order, rest_client: RestClient, backend_base_url: str) -> None:
    order = make_order()

    with allure.step("PUT /api/order/customerOrders — status=Processing"):
        rest_client.put(
            f"{backend_base_url}/api/order/customerOrders",
            json={**order, "status": "Processing"},
        )

    with allure.step("Verify status changed via GET"):
        reloaded = rest_client.get(f"{backend_base_url}/api/order/customerOrders/{order['id']}")
        assert reloaded["status"] == "Processing"


@pytest.mark.restapi
@allure.feature("Orders (REST API)")
@allure.title("Get order by non-existent id — expect empty or 404")
def test_order_get_not_found(rest_client: RestClient, backend_base_url: str) -> None:
    bogus_id = f"qa-missing-{uuid.uuid4().hex}"

    with allure.step(f"GET /api/order/customerOrders/{bogus_id}"):
        try:
            result = rest_client.get(f"{backend_base_url}/api/order/customerOrders/{bogus_id}")
        except HTTPError as exc:
            assert exc.response.status_code in (404, 204)
        else:
            assert result is None or result.get("id") != bogus_id
