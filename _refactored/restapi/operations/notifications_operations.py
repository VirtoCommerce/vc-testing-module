"""REST API operations for VirtoCommerce push notifications."""

from typing import Any

from restapi.operations.base import RestBaseOperations


class NotificationsOperations(RestBaseOperations):
    PATH = "/api/platform/pushnotifications"

    def search(self, *, skip: int = 0, take: int = 20, **extra: Any) -> dict:
        """GET /api/platform/pushnotifications."""
        params: dict[str, Any] = {"skip": skip, "take": take, **extra}
        return self._client.get(self._url(self.PATH), params=params)

    def mark_all_as_read(self) -> None:
        """POST /api/platform/pushnotifications/markallasread."""
        self._client.post(self._url(f"{self.PATH}/markallasread"), json={})
