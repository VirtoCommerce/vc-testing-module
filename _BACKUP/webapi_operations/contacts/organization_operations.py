"""REST API operations for VirtoCommerce organizations (member module).

Wraps the /api/members endpoints for organization CRUD. Organizations are a
member type in the VirtoCommerce member module, sharing endpoints with contacts
and other member types.
"""

from typing import Any

from fixtures.webapi_client import WebAPISession
from tests_webapi.constants import ORGANIZATION_TEMPLATE


class OrganizationOperations:
    """Operations on /api/members for memberType=Organization."""

    BASE = "/api/members"

    def __init__(self, client: WebAPISession) -> None:
        self.client = client

    def create(self, *, name: str, **overrides: Any) -> dict:
        """POST /api/members — create an organization.

        Builds the payload from ORGANIZATION_TEMPLATE. Caller supplies a unique
        `name` (include a uuid suffix for parallel safety). Any extra keyword
        argument overrides a template field.
        """
        payload = {**ORGANIZATION_TEMPLATE, "name": name, **overrides}
        return self.client.post(self.BASE, data=payload)

    def get_by_id(self, organization_id: str) -> dict:
        """GET /api/members/{id}."""
        return self.client.get(f"{self.BASE}/{organization_id}")

    def update(self, organization: dict, **overrides: Any) -> dict:
        """PUT /api/members — update an organization.

        Pass the full organization dict returned by `create` or `get_by_id`,
        plus any fields to override.
        """
        payload = {**ORGANIZATION_TEMPLATE, **organization, **overrides}
        return self.client.put(self.BASE, data=payload)

    def search(self, *, keyword: str | None = None, skip: int = 0, take: int = 20, **extra: Any) -> dict:
        """POST /api/members/search.

        Returns {"results": [...], "totalCount": N}.
        The member search endpoint uses `searchPhrase` (not `keyword`).
        """
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
        return self.client.post(f"{self.BASE}/search", data=payload)

    def delete(self, organization_id: str) -> None:
        """DELETE /api/members?ids={id}. Returns 204 No Content."""
        self.client.delete(self.BASE, params={"ids": [organization_id]})
