"""REST API operations for VirtoCommerce pricelist assignments.

Endpoints verified from Katalon Object Repository:
  POST   /api/pricing/assignments                     — create
  PUT    /api/pricing/assignments                     — update
  GET    /api/pricing/assignments?pricelistIds=       — search by pricelist
  GET    /api/pricing/assignments/{id}                — get by id
  GET    /api/pricing/assignments/new                 — get new (template)
  DELETE /api/pricing/assignments?ids=                — delete
  DELETE /api/pricing/filteredAssignments?SearchPhrase= — delete filtered
"""

from typing import Any

from restapi.operations.base import RestBaseOperations
from restapi.types import PricelistAssignment


class PricelistAssignmentOperations(RestBaseOperations):
    PATH = "/api/pricing/assignments"

    def create(self, *, pricelist_id: str, catalog_id: str, name: str, **overrides: Any) -> PricelistAssignment:
        payload: dict[str, Any] = {
            "pricelistId": pricelist_id,
            "catalogId": catalog_id,
            "name": name,
            **overrides,
        }
        response = self._client.post(self._url(self.PATH), json=payload)
        return PricelistAssignment.model_validate(response)

    def update(self, assignment: PricelistAssignment, **overrides: Any) -> None:
        """PUT returns 204 No Content; tests re-fetch via get_by_id to verify."""
        existing = assignment.model_dump(by_alias=True, exclude_none=True)
        self._client.put(self._url(self.PATH), json={**existing, **overrides})

    def search(self, *, pricelist_id: str) -> dict | list:
        """GET /api/pricing/assignments?pricelistIds=..."""
        return self._client.get(self._url(self.PATH), params={"pricelistIds": pricelist_id})

    def get_by_id(self, assignment_id: str) -> PricelistAssignment:
        response = self._client.get(self._url(f"{self.PATH}/{assignment_id}"))
        return PricelistAssignment.model_validate(response)

    def get_new(self) -> dict:
        """GET /api/pricing/assignments/new — returns a template (partial fields, dict)."""
        return self._client.get(self._url(f"{self.PATH}/new"))

    def delete(self, *assignment_ids: str) -> None:
        self._client.delete(self._url(self.PATH), params={"ids": list(assignment_ids)})

    def delete_filtered(self, search_phrase: str) -> None:
        """DELETE /api/pricing/filteredAssignments?SearchPhrase=..."""
        self._client.delete(self._url("/api/pricing/filteredAssignments"), params={"SearchPhrase": search_phrase})
