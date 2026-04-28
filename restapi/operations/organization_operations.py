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
from restapi.types import Organization


class OrganizationOperations(RestBaseOperations):
    PATH = "/api/organizations"

    def create(self, *, name: str, **overrides: Any) -> Organization:
        payload = {**ORGANIZATION_TEMPLATE, "name": name, **overrides}
        response = self._client.post(self._url(self.PATH), json=payload)
        return Organization.model_validate(response)

    def create_bulk(self, organizations: list[dict]) -> list[Organization]:
        response = self._client.post(self._url(f"{self.PATH}/bulk"), json=organizations)
        return [Organization.model_validate(o) for o in response or []]

    def get_by_id(self, org_id: str) -> Organization:
        response = self._client.get(self._url(f"{self.PATH}/{org_id}"))
        return Organization.model_validate(response)

    def get_by_ids(self, org_ids: list[str]) -> list[Organization]:
        response = self._client.get(self._url(self.PATH), params={"ids": org_ids})
        return [Organization.model_validate(o) for o in response or []]

    def update(self, organization: Organization, **overrides: Any) -> None:
        """PUT returns 204 No Content; tests re-fetch via get_by_id to verify."""
        existing = organization.model_dump(by_alias=True, exclude_none=True)
        self._client.put(self._url(self.PATH), json={**existing, **overrides})

    def update_bulk(self, organizations: list[dict]) -> list[Organization]:
        response = self._client.put(self._url(f"{self.PATH}/bulk"), json=organizations)
        return [Organization.model_validate(o) for o in response or []]

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
