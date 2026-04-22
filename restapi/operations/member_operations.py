"""REST API operations for VirtoCommerce generic members.

Endpoints verified from Katalon Object Repository:
  POST   /api/members             — create
  POST   /api/members/bulk        — create bulk
  PUT    /api/members             — update
  PUT    /api/members/bulk        — update bulk
  GET    /api/members/{id}        — get by id
  GET    /api/members?ids=&responseGroup=&memberTypes= — get by ids with group
  POST   /api/members/search      — search
  DELETE /api/members?ids=        — delete
  POST   /api/members/delete      — delete bulk
  GET    /api/members/{orgId}/organizations?id={memberId} — get all in org
  GET    /api/members/organizations — get organizations
"""

from typing import Any

from restapi.operations.base import RestBaseOperations


class MemberOperations(RestBaseOperations):
    PATH = "/api/members"

    def create(self, *, member_type: str, name: str, **overrides: Any) -> dict:
        payload: dict[str, Any] = {"memberType": member_type, "name": name, **overrides}
        return self._client.post(self._url(self.PATH), json=payload)

    def create_bulk(self, members: list[dict]) -> list[dict]:
        return self._client.post(self._url(f"{self.PATH}/bulk"), json=members)

    def get_by_id(self, member_id: str) -> dict:
        return self._client.get(self._url(f"{self.PATH}/{member_id}"))

    def get_by_ids(self, member_ids: list[str], response_group: str = "", member_types: str = "") -> list[dict]:
        return self._client.get(
            self._url(self.PATH),
            params={"ids": member_ids, "responseGroup": response_group, "memberTypes": member_types},
        )

    def update(self, member: dict, **overrides: Any) -> dict:
        payload = {**member, **overrides}
        return self._client.put(self._url(self.PATH), json=payload)

    def update_bulk(self, members: list[dict]) -> list[dict]:
        return self._client.put(self._url(f"{self.PATH}/bulk"), json=members)

    def search(
        self, *, keyword: str | None = None, member_type: str | None = None, skip: int = 0, take: int = 20, **extra: Any
    ) -> dict:
        payload: dict[str, Any] = {"deepSearch": True, "sort": "name:asc", "skip": skip, "take": take, **extra}
        if keyword is not None:
            payload["searchPhrase"] = keyword
        if member_type is not None:
            payload["memberType"] = member_type
        return self._client.post(self._url(f"{self.PATH}/search"), json=payload)

    def delete(self, *member_ids: str) -> None:
        self._client.delete(self._url(self.PATH), params={"ids": list(member_ids)})

    def delete_bulk(self, member_ids: list[str]) -> None:
        self._client.post(self._url(f"{self.PATH}/delete"), json=member_ids)

    def get_all_in_organization(self, org_id: str, member_id: str) -> dict:
        return self._client.get(self._url(f"{self.PATH}/{org_id}/organizations"), params={"id": member_id})

    def get_organizations(self) -> list[dict]:
        return self._client.get(self._url(f"{self.PATH}/organizations"))
