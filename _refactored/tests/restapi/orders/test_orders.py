"""Orders module — migrated from Katalon `API Coverage/ModuleOrders/*`.

Katalon scripts:
  OrderCreate → test_order_create
"""

import uuid

import allure
import pytest

from core.clients.rest import RestClient
from core.global_settings import GlobalSettings


@pytest.mark.restapi
@allure.feature("Orders (REST API)")
@allure.title("Create order")
def test_order_create(
    rest_client: RestClient, backend_base_url: str, global_settings: GlobalSettings, dataset: dict
) -> None:
    order_number = f"QA-{uuid.uuid4().hex[:8].upper()}"
    users = dataset.get("users", [])
    customer_id = users[0]["id"] if users else "unknown-user"
    customer_name = users[0].get("userName", "QA User") if users else "QA User"

    with allure.step("POST /api/order/customerOrders"):
        result = rest_client.post(
            f"{backend_base_url}/api/order/customerOrders",
            json={
                "number": order_number,
                "storeId": global_settings.store_id,
                "customerId": customer_id,
                "customerName": customer_name,
                "currency": "USD",
                "status": "New",
                "items": [],
            },
        )

    with allure.step("Verify"):
        assert result is not None
        order_id = result.get("id", "")

    with allure.step("Cleanup"):
        if order_id:
            try:
                rest_client.delete(f"{backend_base_url}/api/order/customerOrders", params={"ids": [order_id]})
            except Exception:
                pass


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
