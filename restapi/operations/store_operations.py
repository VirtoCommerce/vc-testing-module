"""REST API operations for VirtoCommerce stores.

Endpoints verified from Katalon Object Repository:
  POST   /api/stores              — create
  PUT    /api/stores              — update
  GET    /api/stores              — get all
  GET    /api/stores/{id}         — get by id
  POST   /api/stores/search       — search
  DELETE /api/stores?ids=         — delete
  GET    /api/stores/allowed/{userId} — get accessible stores
"""

import uuid
from typing import Any

from restapi.operations.base import RestBaseOperations
from restapi.types import Store


class StoreOperations(RestBaseOperations):
    PATH = "/api/stores"

    def create(
        self, *, name: str, store_id: str | None = None, catalog: str = "catalog-acme", **overrides: Any
    ) -> Store:
        payload: dict[str, Any] = {
            "id": store_id or f"qa-store-{uuid.uuid4().hex[:8]}",
            "name": name,
            "catalog": catalog,
            "storeState": "Open",
            **overrides,
        }
        response = self._client.post(self._url(self.PATH), json=payload)
        return Store.model_validate(response)

    def update(self, store: Store, **overrides: Any) -> None:
        """PUT returns 204 No Content; tests re-fetch via get_by_id to verify."""
        existing = store.model_dump(by_alias=True, exclude_none=True)
        self._client.put(self._url(self.PATH), json={**existing, **overrides})

    def get_all(self) -> list[Store]:
        # GET /api/stores was removed in Stable 15; list all stores via POST /api/stores/search.
        response = self._client.post(self._url(f"{self.PATH}/search"), json={"skip": 0, "take": 1000})
        results = response.get("results", []) if isinstance(response, dict) else (response or [])
        return [Store.model_validate(s) for s in results]

    def get_by_id(self, store_id: str) -> Store:
        response = self._client.get(self._url(f"{self.PATH}/{store_id}"))
        return Store.model_validate(response)

    def search(self, *, keyword: str | None = None, skip: int = 0, take: int = 20, **extra: Any) -> dict:
        payload: dict[str, Any] = {"skip": skip, "take": take, **extra}
        if keyword is not None:
            payload["keyword"] = keyword
        return self._client.post(self._url(f"{self.PATH}/search"), json=payload)

    def delete(self, *store_ids: str) -> None:
        self._client.delete(self._url(self.PATH), params={"ids": list(store_ids)})

    def get_accessible(self, user_id: str) -> list[dict]:
        return self._client.get(self._url(f"{self.PATH}/allowed/{user_id}"))
