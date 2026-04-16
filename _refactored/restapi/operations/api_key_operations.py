"""REST API operations for VirtoCommerce user API keys."""

from typing import Any

from restapi.operations.base import RestBaseOperations


class ApiKeyOperations(RestBaseOperations):
    BASE = "/api/platform/security/users"
    API_KEYS = "/api/platform/security/apiaccounts"

    def create(
        self, *, user_id: str, name: str, api_key: str | None = None, is_active: bool = True, **overrides: Any
    ) -> dict:
        """POST /api/platform/security/apiaccounts — create an API key for a user."""
        payload: dict[str, Any] = {
            "userId": user_id,
            "name": name,
            "isActive": is_active,
            **overrides,
        }
        if api_key is not None:
            payload["apiKey"] = api_key
        return self._client.post(self._url(self.API_KEYS), json=payload)

    def get_by_user_id(self, user_id: str) -> list[dict]:
        """GET /api/platform/security/users/{userId}/apiaccounts."""
        return self._client.get(self._url(f"{self.BASE}/{user_id}/apiaccounts"))

    def update(self, api_account: dict, **overrides: Any) -> dict:
        """PUT /api/platform/security/apiaccounts."""
        payload = {**api_account, **overrides}
        return self._client.put(self._url(self.API_KEYS), json=payload)

    def delete(self, api_account_ids: list[str]) -> None:
        """DELETE /api/platform/security/apiaccounts."""
        self._client.delete(self._url(self.API_KEYS), params={"ids": api_account_ids})
