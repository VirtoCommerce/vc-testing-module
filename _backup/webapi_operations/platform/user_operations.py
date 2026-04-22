"""REST API operations for VirtoCommerce platform users.

Wraps the endpoints exercised by Katalon `API Coverage/ModulePlatform/User*`
tests. Unlike catalog entities, platform users use verb-in-URL endpoints
(`/users/create`, `/users/search`) plus a name-based DELETE.
"""

from typing import Any

from fixtures.webapi_client import WebAPISession


class UserOperations:
    """Operations on /api/platform/security/users."""

    BASE = "/api/platform/security/users"

    def __init__(self, client: WebAPISession) -> None:
        self.client = client

    def create(
        self,
        *,
        user_name: str,
        email: str,
        password: str,
        user_type: str = "Manager",
        store_id: str | None = None,
        status: str = "Approved",
        email_confirmed: bool = True,
        roles: list[dict] | None = None,
        **overrides: Any,
    ) -> dict:
        """POST /api/platform/security/users/create. Returns `{succeeded, errors, ...}`."""
        payload: dict[str, Any] = {
            "userType": user_type,
            "userName": user_name,
            "password": password,
            "storeId": store_id,
            "status": status,
            "email": email,
            "roles": roles or [],
            "emailConfirmed": email_confirmed,
            **overrides,
        }
        return self.client.post(f"{self.BASE}/create", data=payload)

    def search(self, *, search_phrase: str, take: int = 20, **extra: Any) -> dict:
        """POST /api/platform/security/users/search. Returns `{users: [...], totalCount}`."""
        payload: dict[str, Any] = {
            "searchPhrase": search_phrase,
            "deepSearch": True,
            "sort": "memberType:asc;name:asc",
            "take": take,
            **extra,
        }
        return self.client.post(f"{self.BASE}/search", data=payload)

    def get_by_name(self, user_name: str) -> dict:
        """GET /api/platform/security/users/{userName}."""
        return self.client.get(f"{self.BASE}/{user_name}")

    def update(self, user: dict, **overrides: Any) -> dict:
        """PUT /api/platform/security/users — update user fields.

        Pass the full user dict returned by `get_by_name` or `search`, plus
        any fields to override. Returns the updated user object.
        """
        payload = {**user, **overrides}
        return self.client.put(self.BASE, data=payload)

    def delete(self, *user_names: str) -> dict:
        """DELETE /api/platform/security/users?names=name1&names=name2."""
        return self.client.delete(self.BASE, params={"names": list(user_names)})
