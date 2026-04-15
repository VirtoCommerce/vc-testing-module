"""REST API operations for VirtoCommerce catalog products.

Wraps the endpoints exercised by Katalon `API Coverage/ModuleCatalog/product*`
tests. Product DELETE is performed via the shared
`/api/catalog/listentries/delete` endpoint, same as category DELETE.

Product GET uses the `?ids=` query-string form and returns an array.
"""

from typing import Any

from fixtures.webapi_client import WebAPISession
from tests_webapi.constants import PRODUCT_TEMPLATE


class ProductOperations:
    """Operations on /api/catalog/products."""

    BASE = "/api/catalog/products"
    LIST_ENTRIES_DELETE = "/api/catalog/listentries/delete"

    def __init__(self, client: WebAPISession) -> None:
        self.client = client

    def create(
        self,
        *,
        catalog_id: str,
        category_id: str,
        name: str,
        code: str,
        **overrides: Any,
    ) -> dict:
        """POST /api/catalog/products."""
        payload = {
            **PRODUCT_TEMPLATE,
            "catalogId": catalog_id,
            "categoryId": category_id,
            "name": name,
            "code": code,
            **overrides,
        }
        return self.client.post(self.BASE, data=payload)

    def get_by_ids(self, product_ids: list[str]) -> list[dict]:
        """GET /api/catalog/products?ids=... — returns a list."""
        return self.client.get(self.BASE, params={"ids": product_ids})

    def get_by_id(self, product_id: str) -> dict:
        """Convenience wrapper around get_by_ids for the single-id case."""
        result = self.get_by_ids([product_id])
        if not result:
            raise ValueError(f"Product {product_id} not found")
        return result[0]

    def update(self, product: dict, **overrides: Any) -> dict:
        """POST /api/catalog/products (same endpoint as create; `id` field triggers update)."""
        payload = {**PRODUCT_TEMPLATE, **product, **overrides}
        return self.client.post(self.BASE, data=payload)

    def delete(self, product_id: str) -> None:
        """POST /api/catalog/listentries/delete with product id in objectIds."""
        self.client.post(self.LIST_ENTRIES_DELETE, data={"objectIds": [product_id]})
