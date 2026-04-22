"""REST API operations for VirtoCommerce catalog products."""

from typing import Any

from restapi.constants import PRODUCT_TEMPLATE
from restapi.operations.base import RestBaseOperations


class ProductOperations(RestBaseOperations):
    PATH = "/api/catalog/products"
    LIST_ENTRIES_DELETE = "/api/catalog/listentries/delete"
    LIST_ENTRIES_MOVE = "/api/catalog/listentries/move"

    def create(self, *, catalog_id: str, category_id: str, name: str, code: str, **overrides: Any) -> dict:
        payload = {
            **PRODUCT_TEMPLATE,
            "catalogId": catalog_id,
            "categoryId": category_id,
            "name": name,
            "code": code,
            **overrides,
        }
        return self._client.post(self._url(self.PATH), json=payload)

    def get_by_ids(self, product_ids: list[str]) -> list[dict]:
        return self._client.get(self._url(self.PATH), params={"ids": product_ids})

    def get_by_id(self, product_id: str) -> dict:
        result = self.get_by_ids([product_id])
        if not result:
            raise ValueError(f"Product {product_id} not found")
        return result[0]

    def update(self, product: dict, **overrides: Any) -> dict:
        payload = {**PRODUCT_TEMPLATE, **product, **overrides}
        return self._client.post(self._url(self.PATH), json=payload)

    def create_or_update_with_body(self, body: dict) -> dict:
        return self._client.post(self._url(self.PATH), json=body)

    def get_clone(self, product_id: str) -> dict:
        return self._client.get(self._url(f"{self.PATH}/{product_id}/clone"))

    def move(self, *, target_catalog_id: str, list_entries: list[dict]) -> None:
        payload = {"catalog": target_catalog_id, "listEntries": list_entries}
        self._client.post(self._url(self.LIST_ENTRIES_MOVE), json=payload)

    def delete(self, product_id: str) -> None:
        self._client.post(self._url(self.LIST_ENTRIES_DELETE), json={"objectIds": [product_id]})
