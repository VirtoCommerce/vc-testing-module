"""Orders module fixtures — operations + factory fixtures."""

import copy
import uuid
from typing import Any, Callable, Generator

import pytest

from core.clients.rest import RestClient
from core.global_settings import GlobalSettings
from restapi.constants import ORDER_LINE_ITEM_TEMPLATE, ORDER_TEMPLATE
from restapi.operations import OrderOperations
from restapi.types import CustomerOrder


@pytest.fixture
def order_ops(rest_client: RestClient, backend_base_url: str) -> OrderOperations:
    return OrderOperations(rest_client, backend_base_url)


@pytest.fixture(scope="session")
def seed_order_customer(dataset: dict) -> dict:
    """First seeded user — used as customer on factory-created orders."""
    users = dataset.get("users") or []
    if not users:
        pytest.skip("No seeded users in dataset")
    return users[0]


@pytest.fixture
def make_order(
    order_ops: OrderOperations,
    global_settings: GlobalSettings,
    seed_order_customer: dict,
) -> Generator[Callable[..., CustomerOrder], None, None]:
    """Factory: create a customer order; deletes everything created at teardown.

    Defaults produce an empty-items order suitable for basic CRUD/search tests.
    Pass `with_item=True` for an order containing the seeded reference line item
    (required by payments/new, shipments/new, recalculate flows).
    """
    created_ids: list[str] = []

    def _make(*, with_item: bool = False, **overrides: Any) -> CustomerOrder:
        items: list[dict] = []
        if with_item:
            line_item = {**copy.deepcopy(ORDER_LINE_ITEM_TEMPLATE), "id": str(uuid.uuid4())}
            items = [line_item]

        payload: dict[str, Any] = {
            **copy.deepcopy(ORDER_TEMPLATE),
            "id": str(uuid.uuid4()),
            "number": f"QA-{uuid.uuid4().hex[:8].upper()}",
            "storeId": global_settings.store_id,
            "customerId": seed_order_customer["id"],
            "customerName": seed_order_customer.get("userName", "QA User"),
            "createdBy": seed_order_customer.get("userName", "admin"),
            "items": items,
        }
        payload.update(overrides)

        order = order_ops.create(payload)
        created_ids.append(order.id)
        return order

    yield _make

    for oid in reversed(created_ids):
        try:
            order_ops.delete(oid)
        except Exception:
            pass
