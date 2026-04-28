"""REST API operations for VirtoCommerce contacts.

Endpoints verified from Katalon Object Repository:
  POST   /api/contacts           — create
  POST   /api/contacts/bulk      — create bulk
  PUT    /api/contacts           — update
  PUT    /api/contacts/bulk      — update bulk
  GET    /api/contacts/{id}      — get by id
  GET    /api/contacts?ids=      — get bulk by ids
  POST   /api/contacts/search    — search
  DELETE /api/contacts?ids=      — delete
  PUT    /api/addresses?memberId= — update addresses
"""

from typing import Any

from restapi.constants import CONTACT_TEMPLATE
from restapi.operations.base import RestBaseOperations
from restapi.types import Contact


class ContactOperations(RestBaseOperations):
    PATH = "/api/contacts"

    def create(self, *, first_name: str, last_name: str, **overrides: Any) -> Contact:
        payload = {
            **CONTACT_TEMPLATE,
            "firstName": first_name,
            "lastName": last_name,
            "name": f"{first_name} {last_name}",
            **overrides,
        }
        response = self._client.post(self._url(self.PATH), json=payload)
        return Contact.model_validate(response)

    def create_bulk(self, contacts: list[dict]) -> list[Contact]:
        response = self._client.post(self._url(f"{self.PATH}/bulk"), json=contacts)
        return [Contact.model_validate(c) for c in response or []]

    def get_by_id(self, contact_id: str) -> Contact:
        response = self._client.get(self._url(f"{self.PATH}/{contact_id}"))
        return Contact.model_validate(response)

    def get_by_ids(self, contact_ids: list[str]) -> list[Contact]:
        response = self._client.get(self._url(self.PATH), params={"ids": contact_ids})
        return [Contact.model_validate(c) for c in response or []]

    def update(self, contact: Contact, **overrides: Any) -> None:
        """PUT returns 204 No Content; tests re-fetch via get_by_id to verify."""
        existing = contact.model_dump(by_alias=True, exclude_none=True)
        self._client.put(self._url(self.PATH), json={**existing, **overrides})

    def update_bulk(self, contacts: list[dict]) -> list[Contact]:
        response = self._client.put(self._url(f"{self.PATH}/bulk"), json=contacts)
        return [Contact.model_validate(c) for c in response or []]

    def search(self, *, keyword: str | None = None, skip: int = 0, take: int = 20, **extra: Any) -> dict:
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
        return self._client.post(self._url(f"{self.PATH}/search"), json=payload)

    def delete(self, *contact_ids: str) -> None:
        self._client.delete(self._url(self.PATH), params={"ids": list(contact_ids)})

    def update_addresses(self, member_id: str, addresses: list[dict]) -> None:
        self._client.put(self._url("/api/addresses"), params={"memberId": member_id}, json=addresses)
