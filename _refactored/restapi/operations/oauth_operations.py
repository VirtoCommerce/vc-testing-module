"""REST API operations for VirtoCommerce OAuth clients."""

from typing import Any

from restapi.operations.base import RestBaseOperations


class OAuthOperations(RestBaseOperations):
    PATH = "/api/platform/oauthapps"

    def create(self, *, client_id: str, client_secret: str, display_name: str | None = None, **overrides: Any) -> dict:
        """POST /api/platform/oauthapps."""
        payload: dict[str, Any] = {
            "clientId": client_id,
            "clientSecret": client_secret,
            "displayName": display_name or client_id,
            **overrides,
        }
        return self._client.post(self._url(self.PATH), json=payload)

    def search(self, *, skip: int = 0, take: int = 20, **extra: Any) -> dict:
        """POST /api/platform/oauthapps/search."""
        payload: dict[str, Any] = {"skip": skip, "take": take, **extra}
        return self._client.post(self._url(f"{self.PATH}/search"), json=payload)

    def delete(self, client_id: str) -> None:
        """DELETE /api/platform/oauthapps?clientIds={clientId}."""
        self._client.delete(self._url(self.PATH), params={"clientIds": [client_id]})
