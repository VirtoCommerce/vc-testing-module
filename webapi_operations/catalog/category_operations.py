"""REST API operations for VirtoCommerce catalog categories.

Wraps the endpoints exercised by Katalon `API Coverage/ModuleCatalog/category*`
tests. Note that category DELETE is performed via the shared
`/api/catalog/listentries/delete` endpoint, same as product DELETE.
"""

from typing import Any

from fixtures.webapi_client import WebAPISession
from tests_webapi.constants import CATEGORY_TEMPLATE


class CategoryOperations:
    """Operations on /api/catalog/categories."""

    BASE = "/api/catalog/categories"
    LIST_ENTRIES_DELETE = "/api/catalog/listentries/delete"

    def __init__(self, client: WebAPISession) -> None:
        self.client = client

    def create(self, *, catalog_id: str, name: str, code: str, **overrides: Any) -> dict:
        """POST /api/catalog/categories."""
        payload = {
            **CATEGORY_TEMPLATE,
            "catalogId": catalog_id,
            "name": name,
            "code": code,
            **overrides,
        }
        return self.client.post(self.BASE, data=payload)

    def get_by_id(self, category_id: str) -> dict:
        """GET /api/catalog/categories/{id}."""
        return self.client.get(f"{self.BASE}/{category_id}")

    def update(self, category: dict, **overrides: Any) -> dict:
        """POST /api/catalog/categories (same endpoint as create; `id` field triggers update)."""
        payload = {**CATEGORY_TEMPLATE, **category, **overrides}
        return self.client.post(self.BASE, data=payload)

    def delete(self, category_id: str) -> None:
        """POST /api/catalog/listentries/delete with category id in objectIds."""
        self.client.post(self.LIST_ENTRIES_DELETE, data={"objectIds": [category_id]})
