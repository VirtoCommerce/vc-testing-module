"""REST API operations for VirtoCommerce catalogs."""

from typing import Any

from restapi.constants import CATALOG_TEMPLATE
from restapi.operations.base import RestBaseOperations


class CatalogOperations(RestBaseOperations):
    PATH = "/api/catalog/catalogs"

    def create(self, *, name: str, **overrides: Any) -> dict:
        payload = {**CATALOG_TEMPLATE, "name": name, **overrides}
        return self._client.post(self._url(self.PATH), json=payload)

    def update(self, catalog: dict, **overrides: Any) -> dict:
        payload = {
            **CATALOG_TEMPLATE,
            **catalog,
            "properties": catalog.get("properties") or [],
            **overrides,
        }
        return self._client.put(self._url(self.PATH), json=payload)

    def search(self, *, keyword: str | None = None, skip: int = 0, take: int = 20, **extra: Any) -> dict:
        payload: dict[str, Any] = {"sort": "name:asc", "skip": skip, "take": take, **extra}
        if keyword is not None:
            payload["keyword"] = keyword
        return self._client.post(self._url(f"{self.PATH}/search"), json=payload)

    def delete(self, catalog_id: str) -> None:
        self._client.delete(self._url(f"{self.PATH}/{catalog_id}"))
