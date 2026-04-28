"""REST API operations for VirtoCommerce orders.

Endpoints verified from Katalon Object Repository
(Object Repository/API/backWebServices/VirtoCommerce.Order/*.rs):
  POST   /api/order/customerOrders                          — create
  GET    /api/order/customerOrders/{id}                     — get by id
  GET    /api/order/customerOrders/number/{number}          — get by number
  PUT    /api/order/customerOrders                          — update (204)
  PUT    /api/order/customerOrders/recalculate              — recalculate
  DELETE /api/order/customerOrders?ids=                     — delete
  POST   /api/order/customerOrders/search                   — search
  POST   /api/order/customerOrders/searchChanges            — search changes
  GET    /api/order/customerOrders/{id}/payments/new        — generate new payment
  GET    /api/order/customerOrders/{id}/shipments/new       — generate new shipment
  GET    /api/order/customerOrders/{id}/changes             — changes by order id
  GET    /api/order/customerOrders/indexed/searchEnabled    — indexed search flag
  GET    /api/order/dashboardStatistics?start=&end=         — dashboard stats
  POST   /api/order/customerOrders/{id}/processPayment/{paymentId} — process payment

Read paths (create/get_by_id/get_by_number) return `CustomerOrder`.
Mutation/recalculate paths keep dict in/out so tests can round-trip the
full server response with deep field-level edits (e.g. items[0].quantity)
without paying the cost of dump/reconstruct on every step.
"""

from typing import Any

from restapi.operations.base import RestBaseOperations
from restapi.types import CustomerOrder


class OrderOperations(RestBaseOperations):
    PATH = "/api/order/customerOrders"

    def create(self, payload: dict) -> CustomerOrder:
        response = self._client.post(self._url(self.PATH), json=payload)
        return CustomerOrder.model_validate(response)

    def get_by_id(self, order_id: str) -> CustomerOrder:
        response = self._client.get(self._url(f"{self.PATH}/{order_id}"))
        return CustomerOrder.model_validate(response)

    def get_by_number(self, order_number: str) -> CustomerOrder:
        response = self._client.get(self._url(f"{self.PATH}/number/{order_number}"))
        return CustomerOrder.model_validate(response)

    def update(self, order: dict | CustomerOrder) -> None:
        body = order.model_dump(by_alias=True) if isinstance(order, CustomerOrder) else order
        self._client.put(self._url(self.PATH), json=body)

    def recalculate(self, order: dict | CustomerOrder) -> dict:
        body = order.model_dump(by_alias=True) if isinstance(order, CustomerOrder) else order
        return self._client.put(self._url(f"{self.PATH}/recalculate"), json=body)

    def delete(self, *order_ids: str) -> None:
        self._client.delete(self._url(self.PATH), params={"ids": list(order_ids)})

    def search(self, *, keyword: str | None = None, skip: int = 0, take: int = 20, **extra: Any) -> dict:
        payload: dict[str, Any] = {"skip": skip, "take": take, **extra}
        if keyword is not None:
            payload["keyword"] = keyword
        return self._client.post(self._url(f"{self.PATH}/search"), json=payload)

    def search_changes(self, *, order_id: str, skip: int = 0, take: int = 10) -> dict:
        return self._client.post(
            self._url(f"{self.PATH}/searchChanges"),
            json={"orderId": order_id, "skip": skip, "take": take},
        )

    def get_new_payment(self, order_id: str) -> dict:
        return self._client.get(self._url(f"{self.PATH}/{order_id}/payments/new"))

    def get_new_shipment(self, order_id: str) -> dict:
        return self._client.get(self._url(f"{self.PATH}/{order_id}/shipments/new"))

    def get_changes(self, order_id: str) -> dict:
        return self._client.get(self._url(f"{self.PATH}/{order_id}/changes"))

    def indexed_search_enabled(self) -> dict:
        return self._client.get(self._url(f"{self.PATH}/indexed/searchEnabled"))

    def dashboard_statistics(self, *, start: str, end: str) -> dict:
        return self._client.get(
            self._url("/api/order/dashboardStatistics"),
            params={"start": start, "end": end},
        )

    def process_payment(self, *, order_id: str, payment_id: str, payload: dict | None = None) -> dict | None:
        return self._client.post(
            self._url(f"{self.PATH}/{order_id}/processPayment/{payment_id}"),
            json=payload or {},
        )
