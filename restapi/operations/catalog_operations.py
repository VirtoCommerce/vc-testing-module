"""REST API operations for VirtoCommerce catalogs."""

from typing import Any

from restapi.constants import CATALOG_TEMPLATE
from restapi.operations.base import RestBaseOperations
from restapi.types import Catalog


class CatalogOperations(RestBaseOperations):
    PATH = "/api/catalog/catalogs"

    def create(self, *, name: str, **overrides: Any) -> Catalog:
        payload = {**CATALOG_TEMPLATE, "name": name, **overrides}
        response = self._client.post(self._url(self.PATH), json=payload)
        return Catalog.model_validate(response)

    def update(self, catalog: Catalog, **overrides: Any) -> Catalog:
        existing = catalog.model_dump(by_alias=True, exclude_none=True)
        payload = {
            **CATALOG_TEMPLATE,
            **existing,
            "properties": existing.get("properties") or [],
            **overrides,
        }
        response = self._client.put(self._url(self.PATH), json=payload)
        return Catalog.model_validate(response)

    def search(self, *, keyword: str | None = None, skip: int = 0, take: int = 20, **extra: Any) -> dict:
        payload: dict[str, Any] = {"sort": "name:asc", "skip": skip, "take": take, **extra}
        if keyword is not None:
            payload["keyword"] = keyword
        return self._client.post(self._url(f"{self.PATH}/search"), json=payload)

    def delete(self, catalog_id: str) -> None:
        self._client.delete(self._url(f"{self.PATH}/{catalog_id}"))
