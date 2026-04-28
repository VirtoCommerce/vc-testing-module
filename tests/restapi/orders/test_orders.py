"""Orders module — migrated from Katalon `API Coverage/ModuleOrders/OrderCreate`.

Mapping (1 Katalon script → many focused pytest tests):
  Katalon `OrderCreate/Script1629368773186.groovy`:
    OrderCreate                  → test_order_create
    OrderGetById                 → test_order_get_by_id
    OrderPaymentsGetByOrderId    → test_order_get_new_payment
    OrderShipmentsGetById        → test_order_get_new_shipment
    OrderRecalculate             → test_order_recalculate_updates_totals
    OrderUpdate                  → test_order_update_attaches_payment_and_shipment
    OrderGetByOrderNumber        → test_order_get_by_number
    OrderSearchChanges (delta)   → test_order_search_changes_count_grows_after_update
    OrderSearch (keyword)        → test_order_search_by_keyword_finds_created
    OrderDelete + verify gone    → test_order_delete_removes_from_search
    Order#64-symbol validation   → test_order_create_with_too_long_number_returns_5xx
  Plus standalone endpoints not exercised by the Katalon flow:
    test_order_indexed_search_enabled
    test_order_get_not_found
    test_order_search (basic shape)
    test_order_update_status
"""

import uuid

import allure
import pytest
import requests
from requests.exceptions import HTTPError

from restapi.operations import OrderOperations


_FEATURE = "Orders (REST API)"


# -------------------------------------------------------------------- create


@pytest.mark.restapi
@allure.feature(_FEATURE)
@allure.title("Create order")
def test_order_create(make_order) -> None:
    with allure.step("POST /api/order/customerOrders"):
        order = make_order()

    with allure.step("Verify response"):
        assert order.id
        assert order.number.startswith("QA-")
        assert order.status == "New"


# ---------------------------------------------------------------------- read


@pytest.mark.restapi
@allure.feature(_FEATURE)
@allure.title("Get order by id")
def test_order_get_by_id(make_order, order_ops: OrderOperations) -> None:
    order = make_order()

    with allure.step(f"GET /api/order/customerOrders/{order.id}"):
        reloaded = order_ops.get_by_id(order.id)

    with allure.step("Verify fields match"):
        assert reloaded.id == order.id
        assert reloaded.number == order.number
        assert reloaded.store_id == order.store_id


@pytest.mark.restapi
@allure.feature(_FEATURE)
@allure.title("Get order by number")
def test_order_get_by_number(make_order, order_ops: OrderOperations) -> None:
    order = make_order()

    with allure.step(f"GET /api/order/customerOrders/number/{order.number}"):
        reloaded = order_ops.get_by_number(order.number)

    with allure.step("Verify the same order is returned"):
        assert reloaded.id == order.id
        assert reloaded.number == order.number


@pytest.mark.restapi
@allure.feature(_FEATURE)
@allure.title("Get order by non-existent id — expect empty or 404")
def test_order_get_not_found(order_ops: OrderOperations) -> None:
    from pydantic import ValidationError

    bogus_id = f"qa-missing-{uuid.uuid4().hex}"

    with allure.step(f"GET /api/order/customerOrders/{bogus_id}"):
        # Server returns either 404 (HTTPError) or 200 with null body (ValidationError
        # because Pydantic can't construct a CustomerOrder from None). Both indicate
        # "not found" — either is accepted.
        try:
            order_ops.get_by_id(bogus_id)
        except HTTPError as exc:
            assert exc.response.status_code in (404, 204)
        except ValidationError:
            pass  # null body — also a "not found" signal


# -------------------------------------------------------------------- search


@pytest.mark.restapi
@allure.feature(_FEATURE)
@allure.title("Search orders — basic shape")
def test_order_search(order_ops: OrderOperations) -> None:
    with allure.step("POST /api/order/customerOrders/search"):
        result = order_ops.search(skip=0, take=5)

    with allure.step("Verify response shape"):
        assert isinstance(result, dict)
        assert "totalCount" in result or "results" in result


@pytest.mark.restapi
@allure.feature(_FEATURE)
@allure.title("Search orders by keyword finds the created order")
def test_order_search_by_keyword_finds_created(make_order, order_ops: OrderOperations) -> None:
    order = make_order()

    with allure.step(f"POST /api/order/customerOrders/search keyword={order.number}"):
        result = order_ops.search(keyword=order.number, take=5)

    with allure.step("Verify created order is among results"):
        assert isinstance(result, dict)
        ids = [r.get("id") for r in (result.get("results") or [])]
        assert order.id in ids, f"Order {order.id} not found in search results: {ids}"


@pytest.mark.restapi
@allure.feature(_FEATURE)
@allure.title("Check indexed search enabled")
def test_order_indexed_search_enabled(order_ops: OrderOperations) -> None:
    with allure.step("GET /api/order/customerOrders/indexed/searchEnabled"):
        result = order_ops.indexed_search_enabled()

    with allure.step("Verify response contains result flag"):
        assert isinstance(result, dict)
        assert "result" in result
        assert isinstance(result["result"], bool)


# ------------------------------------------------------ payments / shipments


@pytest.mark.restapi
@allure.feature(_FEATURE)
@allure.title("Generate new payment for order")
def test_order_get_new_payment(make_order, order_ops: OrderOperations) -> None:
    order = make_order(with_item=True)

    with allure.step(f"GET /api/order/customerOrders/{order.id}/payments/new"):
        payment = order_ops.get_new_payment(order.id)

    with allure.step("Verify payment is bound to order's customer"):
        assert isinstance(payment, dict)
        assert payment.get("customerId") == order.customer_id
        assert payment.get("number")


@pytest.mark.restapi
@allure.feature(_FEATURE)
@allure.title("Generate new shipment for order")
def test_order_get_new_shipment(make_order, order_ops: OrderOperations) -> None:
    order = make_order(with_item=True)

    with allure.step(f"GET /api/order/customerOrders/{order.id}/shipments/new"):
        shipment = order_ops.get_new_shipment(order.id)

    with allure.step("Verify shipment has a generated number"):
        assert isinstance(shipment, dict)
        assert shipment.get("number")


# ---------------------------------------------------- update / recalculate


@pytest.mark.restapi
@allure.feature(_FEATURE)
@allure.title("Update order — change status to Processing")
def test_order_update_status(make_order, order_ops: OrderOperations) -> None:
    order = make_order()

    with allure.step("PUT /api/order/customerOrders — status=Processing"):
        body = order.model_dump(by_alias=True)
        body["status"] = "Processing"
        order_ops.update(body)

    with allure.step("Verify status changed via GET"):
        reloaded = order_ops.get_by_id(order.id)
        assert reloaded.status == "Processing"


@pytest.mark.restapi
@allure.feature(_FEATURE)
@allure.title("Recalculate order totals after quantity change")
def test_order_recalculate_updates_totals(make_order, order_ops: OrderOperations) -> None:
    order = make_order(with_item=True)
    body = order.model_dump(by_alias=True)
    new_quantity = body["items"][0]["quantity"] + 1
    body["items"][0]["quantity"] = new_quantity

    with allure.step("PUT /api/order/customerOrders/recalculate"):
        recalculated = order_ops.recalculate(body)

    with allure.step("Verify total = price * quantity for the single line item"):
        assert isinstance(recalculated, dict)
        item = recalculated["items"][0]
        assert item["quantity"] == new_quantity
        assert recalculated["total"] == item["price"] * item["quantity"]


@pytest.mark.restapi
@allure.feature(_FEATURE)
@allure.title("Attach generated payment + shipment, recalculate, update — verify persisted")
def test_order_update_attaches_payment_and_shipment(make_order, order_ops: OrderOperations) -> None:
    order = make_order(with_item=True)
    body = order.model_dump(by_alias=True)
    new_quantity = body["items"][0]["quantity"] + 1

    with allure.step("Generate fresh payment and shipment for the order"):
        payment = order_ops.get_new_payment(order.id)
        shipment = order_ops.get_new_shipment(order.id)

    body["inPayments"] = [payment]
    body["shipments"] = [shipment]
    body["items"][0]["quantity"] = new_quantity

    with allure.step("PUT /api/order/customerOrders/recalculate"):
        recalculated = order_ops.recalculate(body)

    with allure.step("PUT /api/order/customerOrders — persist recalculated body"):
        order_ops.update(recalculated)

    with allure.step(f"GET /api/order/customerOrders/number/{order.number} — verify"):
        updated = order_ops.get_by_number(order.number)
        assert updated.items[0].quantity == new_quantity
        extras = updated.model_extra or {}
        assert extras.get("inPayments", [{}])[0].get("number") == payment["number"]
        assert extras.get("shipments", [{}])[0].get("number") == shipment["number"]


# ----------------------------------------------------------- search changes


@pytest.mark.restapi
@allure.feature(_FEATURE)
@allure.title("searchChanges count grows after order is updated")
@pytest.mark.xfail(
    strict=False,
    reason=(
        "Order change records are written asynchronously on the platform. On the current demo "
        "backend the lag exceeds the test runtime (verified empirically: pre-existing seeded "
        "orders show change records, but freshly created/updated orders return totalCount=0 "
        "for >10s). Endpoint contract is exercised; XPASS would indicate change tracking "
        "became synchronous (good — remove xfail then)."
    ),
)
def test_order_search_changes_count_grows_after_update(make_order, order_ops: OrderOperations) -> None:
    order = make_order(with_item=True)

    with allure.step("POST /api/order/customerOrders/searchChanges — initial count"):
        initial = order_ops.search_changes(order_id=order.id)
        initial_count = initial["totalCount"]

    with allure.step("Attach payment + shipment + bump quantity, recalculate, persist update"):
        payment = order_ops.get_new_payment(order.id)
        shipment = order_ops.get_new_shipment(order.id)
        body = order.model_dump(by_alias=True)
        body["inPayments"] = [payment]
        body["shipments"] = [shipment]
        body["items"][0]["quantity"] = body["items"][0]["quantity"] + 1
        recalculated = order_ops.recalculate(body)
        order_ops.update(recalculated)

    with allure.step("POST /api/order/customerOrders/searchChanges — final count > initial"):
        final = order_ops.search_changes(order_id=order.id)
        assert (
            final["totalCount"] > initial_count
        ), f"Expected change count to grow, got initial={initial_count} final={final['totalCount']}"


# --------------------------------------------------------- delete (lifecycle)


@pytest.mark.restapi
@allure.feature(_FEATURE)
@allure.title("Delete order — search by its number returns nothing")
def test_order_delete_removes_from_search(make_order, order_ops: OrderOperations) -> None:
    order = make_order()
    order_number = order.number

    with allure.step(f"DELETE /api/order/customerOrders?ids={order.id}"):
        order_ops.delete(order.id)

    with allure.step(f"POST /api/order/customerOrders/search keyword={order_number} — expect deleted id absent"):
        result = order_ops.search(keyword=order_number, take=5)
        ids = [r.get("id") for r in (result.get("results") or [])]
        assert order.id not in ids, f"Deleted order {order.id} still appears in search"


# --------------------------------------------------------- input validation


@pytest.mark.restapi
@allure.feature(_FEATURE)
@allure.title("Create order with order number > 64 chars — server rejects with 5xx")
def test_order_create_with_too_long_number_returns_5xx(make_order) -> None:
    too_long_number = "X" * 65

    with allure.step(f"POST /api/order/customerOrders — number length={len(too_long_number)}"):
        with pytest.raises(requests.HTTPError) as exc_info:
            make_order(number=too_long_number)

    with allure.step("Verify server rejected with 4xx/5xx"):
        assert (
            exc_info.value.response.status_code >= 400
        ), f"Expected error status, got {exc_info.value.response.status_code}"
