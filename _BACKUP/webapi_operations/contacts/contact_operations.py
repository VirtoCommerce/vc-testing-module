"""REST API operations for VirtoCommerce contacts (member module).

Wraps the /api/members endpoints for contact CRUD. Contacts are a member type
in the VirtoCommerce member module, sharing endpoints with organizations and
other member types.
"""

from typing import Any

from fixtures.webapi_client import WebAPISession
from tests_webapi.constants import CONTACT_TEMPLATE


class ContactOperations:
    """Operations on /api/members for memberType=Contact."""

    BASE = "/api/members"

    def __init__(self, client: WebAPISession) -> None:
        self.client = client

    def create(self, *, first_name: str, last_name: str, **overrides: Any) -> dict:
        """POST /api/members — create a contact.

        Builds the payload from CONTACT_TEMPLATE. Caller supplies `first_name`
        and `last_name`. Any extra keyword argument overrides a template field.
        """
        payload = {
            **CONTACT_TEMPLATE,
            "firstName": first_name,
            "lastName": last_name,
            "name": f"{first_name} {last_name}",
            **overrides,
        }
        return self.client.post(self.BASE, data=payload)

    def get_by_id(self, contact_id: str) -> dict:
        """GET /api/members/{id}."""
        return self.client.get(f"{self.BASE}/{contact_id}")

    def update(self, contact: dict, **overrides: Any) -> dict:
        """PUT /api/members — update a contact.

        Pass the full contact dict returned by `create` or `get_by_id`,
        plus any fields to override.
        """
        payload = {**CONTACT_TEMPLATE, **contact, **overrides}
        return self.client.put(self.BASE, data=payload)

    def search(self, *, keyword: str | None = None, skip: int = 0, take: int = 20, **extra: Any) -> dict:
        """POST /api/members/search.

        Returns {"results": [...], "totalCount": N}.
        The member search endpoint uses `searchPhrase` (not `keyword`).
        """
        payload: dict[str, Any] = {
            "memberType": "Contact",
            "deepSearch": True,
            "sort": "name:asc",
            "skip": skip,
            "take": take,
            **extra,
        }
        if keyword is not None:
            payload["searchPhrase"] = keyword
        return self.client.post(f"{self.BASE}/search", data=payload)

    def delete(self, contact_id: str) -> None:
        """DELETE /api/members?ids={id}. Returns 204 No Content."""
        self.client.delete(self.BASE, params={"ids": [contact_id]})
