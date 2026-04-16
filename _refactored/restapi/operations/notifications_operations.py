"""REST API operations for VirtoCommerce push notifications."""

from typing import Any

from restapi.operations.base import RestBaseOperations


class NotificationsOperations(RestBaseOperations):
    PATH = "/api/platform/pushnotifications"

    def search(self, *, skip: int = 0, take: int = 20, **extra: Any) -> dict:
        """POST /api/platform/pushnotifications."""
        payload: dict[str, Any] = {"skip": skip, "take": take, **extra}
        return self._client.post(self._url(self.PATH), json=payload)

    def mark_all_as_read(self) -> None:
        """POST /api/platform/pushnotifications/markAllAsRead."""
        self._client.post(self._url(f"{self.PATH}/markAllAsRead"), json={})
