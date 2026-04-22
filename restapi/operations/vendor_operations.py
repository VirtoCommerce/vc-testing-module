"""REST API operations for VirtoCommerce vendors.

Endpoints verified from Katalon Object Repository:
  GET    /api/vendors/{id}       — get by id
  GET    /api/vendors?ids=       — get bulk by ids
  POST   /api/vendors/search     — search
"""

from typing import Any

from restapi.operations.base import RestBaseOperations


class VendorOperations(RestBaseOperations):
    PATH = "/api/vendors"

    def get_by_id(self, vendor_id: str) -> dict:
        return self._client.get(self._url(f"{self.PATH}/{vendor_id}"))

    def get_by_ids(self, vendor_ids: list[str]) -> list[dict]:
        return self._client.get(self._url(self.PATH), params={"ids": vendor_ids})

    def search(self, *, keyword: str | None = None, skip: int = 0, take: int = 20, **extra: Any) -> dict:
        payload: dict[str, Any] = {"deepSearch": True, "sort": "name:asc", "skip": skip, "take": take, **extra}
        if keyword is not None:
            payload["searchPhrase"] = keyword
        return self._client.post(self._url(f"{self.PATH}/search"), json=payload)
