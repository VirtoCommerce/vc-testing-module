"""REST API operations for VirtoCommerce pricelists.

Endpoints verified from Katalon Object Repository:
  POST   /api/pricing/pricelists              — create
  PUT    /api/pricing/pricelists              — update
  GET    /api/pricing/pricelists?keyword=     — search
  GET    /api/pricing/pricelists/{id}         — get by id
  DELETE /api/pricing/pricelists?ids=         — delete
"""

from typing import Any

from restapi.operations.base import RestBaseOperations
from restapi.types import Pricelist


class PricelistOperations(RestBaseOperations):
    PATH = "/api/pricing/pricelists"

    def create(self, *, name: str, currency: str = "USD", **overrides: Any) -> Pricelist:
        payload: dict[str, Any] = {"name": name, "currency": currency, **overrides}
        response = self._client.post(self._url(self.PATH), json=payload)
        return Pricelist.model_validate(response)

    def update(self, pricelist: Pricelist, **overrides: Any) -> None:
        """PUT returns 204 No Content; tests re-fetch via get_by_id to verify."""
        existing = pricelist.model_dump(by_alias=True, exclude_none=True)
        self._client.put(self._url(self.PATH), json={**existing, **overrides})

    def search(self, *, keyword: str | None = None, skip: int = 0, take: int = 20) -> dict | list:
        params: dict[str, Any] = {"Skip": skip, "Take": take}
        if keyword is not None:
            params["keyword"] = keyword
        return self._client.get(self._url(self.PATH), params=params)

    def get_by_id(self, pricelist_id: str) -> Pricelist:
        response = self._client.get(self._url(f"{self.PATH}/{pricelist_id}"))
        return Pricelist.model_validate(response)

    def delete(self, *pricelist_ids: str) -> None:
        self._client.delete(self._url(self.PATH), params={"ids": list(pricelist_ids)})
