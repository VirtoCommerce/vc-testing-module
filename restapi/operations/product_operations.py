"""REST API operations for VirtoCommerce catalog products."""

from typing import Any

from restapi.constants import PRODUCT_TEMPLATE
from restapi.operations.base import RestBaseOperations
from restapi.types import Product


class ProductOperations(RestBaseOperations):
    PATH = "/api/catalog/products"
    LIST_ENTRIES_DELETE = "/api/catalog/listentries/delete"
    LIST_ENTRIES_MOVE = "/api/catalog/listentries/move"

    def create(self, *, catalog_id: str, category_id: str, name: str, code: str, **overrides: Any) -> Product:
        payload = {
            **PRODUCT_TEMPLATE,
            "catalogId": catalog_id,
            "categoryId": category_id,
            "name": name,
            "code": code,
            **overrides,
        }
        response = self._client.post(self._url(self.PATH), json=payload)
        return Product.model_validate(response)

    def get_by_ids(self, product_ids: list[str]) -> list[Product]:
        response = self._client.get(self._url(self.PATH), params={"ids": product_ids})
        return [Product.model_validate(p) for p in response or []]

    def get_by_id(self, product_id: str) -> Product:
        result = self.get_by_ids([product_id])
        if not result:
            raise ValueError(f"Product {product_id} not found")
        return result[0]

    def update(self, product: Product, **overrides: Any) -> Product:
        existing = product.model_dump(by_alias=True, exclude_none=True)
        payload = {**PRODUCT_TEMPLATE, **existing, **overrides}
        response = self._client.post(self._url(self.PATH), json=payload)
        return Product.model_validate(response)

    def create_or_update_with_body(self, body: dict) -> Product:
        response = self._client.post(self._url(self.PATH), json=body)
        return Product.model_validate(response)

    def get_clone(self, product_id: str) -> dict:
        return self._client.get(self._url(f"{self.PATH}/{product_id}/clone"))

    def move(self, *, target_catalog_id: str, list_entries: list[dict]) -> None:
        payload = {"catalog": target_catalog_id, "listEntries": list_entries}
        self._client.post(self._url(self.LIST_ENTRIES_MOVE), json=payload)

    def delete(self, product_id: str) -> None:
        self._client.post(self._url(self.LIST_ENTRIES_DELETE), json={"objectIds": [product_id]})
