"""REST API operations for VirtoCommerce organizations.

Endpoints verified from Katalon Object Repository:
  POST   /api/organizations           — create
  POST   /api/organizations/bulk      — create bulk
  PUT    /api/organizations           — update
  PUT    /api/organizations/bulk      — update bulk
  GET    /api/organizations/{id}      — get by id
  GET    /api/organizations?ids=      — get bulk by ids
  POST   /api/organizations/search    — search
  DELETE /api/organizations?ids=      — delete
"""

from typing import Any

from restapi.constants import ORGANIZATION_TEMPLATE
from restapi.operations.base import RestBaseOperations


class OrganizationOperations(RestBaseOperations):
    PATH = "/api/organizations"

    def create(self, *, name: str, **overrides: Any) -> dict:
        payload = {**ORGANIZATION_TEMPLATE, "name": name, **overrides}
        return self._client.post(self._url(self.PATH), json=payload)

    def create_bulk(self, organizations: list[dict]) -> list[dict]:
        return self._client.post(self._url(f"{self.PATH}/bulk"), json=organizations)

    def get_by_id(self, org_id: str) -> dict:
        return self._client.get(self._url(f"{self.PATH}/{org_id}"))

    def get_by_ids(self, org_ids: list[str]) -> list[dict]:
        return self._client.get(self._url(self.PATH), params={"ids": org_ids})

    def update(self, organization: dict, **overrides: Any) -> dict:
        payload = {**organization, **overrides}
        return self._client.put(self._url(self.PATH), json=payload)

    def update_bulk(self, organizations: list[dict]) -> list[dict]:
        return self._client.put(self._url(f"{self.PATH}/bulk"), json=organizations)

    def search(self, *, keyword: str | None = None, skip: int = 0, take: int = 20, **extra: Any) -> dict:
        payload: dict[str, Any] = {
            "memberType": "Organization",
            "deepSearch": True,
            "sort": "name:asc",
            "skip": skip,
            "take": take,
            **extra,
        }
        if keyword is not None:
            payload["searchPhrase"] = keyword
        return self._client.post(self._url(f"{self.PATH}/search"), json=payload)

    def delete(self, *org_ids: str) -> None:
        self._client.delete(self._url(self.PATH), params={"ids": list(org_ids)})
