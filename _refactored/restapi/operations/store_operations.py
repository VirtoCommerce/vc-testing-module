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

from typing import Any

from restapi.operations.base import RestBaseOperations


class StoreOperations(RestBaseOperations):
    PATH = "/api/stores"

    def create(
        self, *, name: str, store_id: str | None = None, catalog: str = "catalog-acme", **overrides: Any
    ) -> dict:
        import uuid as _uuid

        payload: dict[str, Any] = {
            "id": store_id or f"qa-store-{_uuid.uuid4().hex[:8]}",
            "name": name,
            "catalog": catalog,
            "storeState": "Open",
            **overrides,
        }
        return self._client.post(self._url(self.PATH), json=payload)

    def update(self, store: dict, **overrides: Any) -> dict:
        return self._client.put(self._url(self.PATH), json={**store, **overrides})

    def get_all(self) -> list[dict]:
        return self._client.get(self._url(self.PATH))

    def get_by_id(self, store_id: str) -> dict:
        return self._client.get(self._url(f"{self.PATH}/{store_id}"))

    def search(self, *, keyword: str | None = None, skip: int = 0, take: int = 20, **extra: Any) -> dict:
        payload: dict[str, Any] = {"skip": skip, "take": take, **extra}
        if keyword is not None:
            payload["keyword"] = keyword
        return self._client.post(self._url(f"{self.PATH}/search"), json=payload)

    def delete(self, *store_ids: str) -> None:
        self._client.delete(self._url(self.PATH), params={"ids": list(store_ids)})

    def get_accessible(self, user_id: str) -> list[dict]:
        return self._client.get(self._url(f"{self.PATH}/allowed/{user_id}"))
