"""REST API operations for VirtoCommerce catalog module.

Wraps the endpoints exercised by the Katalon `API Coverage/ModuleCatalog/*`
test cases: catalog CRUD, category CRUD, product CRUD, channel CRUD, etc.

This module covers Catalogs only. Category / Product / Channel / Tag operations
live in their own sibling modules under `webapi_operations/catalog/`.
"""

from typing import Any

from fixtures.webapi_client import WebAPISession
from tests_webapi.constants import CATALOG_TEMPLATE


class CatalogOperations:
    """Operations on /api/catalog/catalogs."""

    BASE = "/api/catalog/catalogs"

    def __init__(self, client: WebAPISession) -> None:
        self.client = client

    def create(self, *, name: str, **overrides: Any) -> dict:
        """POST /api/catalog/catalogs.

        Builds the payload from CATALOG_TEMPLATE. Caller supplies the unique
        `name` (include a uuid suffix for parallel safety). Any extra keyword
        argument overrides a template field.
        """
        payload = {**CATALOG_TEMPLATE, "name": name, **overrides}
        return self.client.post(self.BASE, data=payload)

    def update(self, catalog: dict, **overrides: Any) -> dict:
        """PUT /api/catalog/catalogs.

        Pass the full catalog dict returned by `create` or `get`, plus any
        fields to override. Ensures `id` and `properties` are set, since the
        Katalon update request explicitly carries them.
        """
        payload = {
            **CATALOG_TEMPLATE,
            **catalog,
            "properties": catalog.get("properties") or [],
            **overrides,
        }
        return self.client.put(self.BASE, data=payload)

    def search(self, *, keyword: str | None = None, skip: int = 0, take: int = 20, **extra: Any) -> dict:
        """POST /api/catalog/catalogs/search.

        Mirrors the Katalon `CatalogsSearch` request body (keyword, sort, skip, take).
        Returns {"results": [...], "totalCount": N}.
        """
        payload: dict[str, Any] = {
            "sort": "name:asc",
            "skip": skip,
            "take": take,
            **extra,
        }
        if keyword is not None:
            payload["keyword"] = keyword
        return self.client.post(f"{self.BASE}/search", data=payload)

    def delete(self, catalog_id: str) -> None:
        """DELETE /api/catalog/catalogs/{id}. Returns 204 No Content."""
        self.client.delete(f"{self.BASE}/{catalog_id}")
