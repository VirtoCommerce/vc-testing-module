"""REST API operations for VirtoCommerce organizations (member module)."""

from typing import Any

from restapi.constants import ORGANIZATION_TEMPLATE
from restapi.operations.base import RestBaseOperations


class OrganizationOperations(RestBaseOperations):
    PATH = "/api/members"

    def create(self, *, name: str, **overrides: Any) -> dict:
        payload = {**ORGANIZATION_TEMPLATE, "name": name, **overrides}
        return self._client.post(self._url(self.PATH), json=payload)

    def get_by_id(self, organization_id: str) -> dict:
        return self._client.get(self._url(f"{self.PATH}/{organization_id}"))

    def update(self, organization: dict, **overrides: Any) -> dict:
        payload = {**ORGANIZATION_TEMPLATE, **organization, **overrides}
        return self._client.put(self._url(self.PATH), json=payload)

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

    def delete(self, organization_id: str) -> None:
        self._client.delete(self._url(self.PATH), params={"ids": [organization_id]})
