"""REST API operations for VirtoCommerce platform settings."""

from typing import Any

from restapi.operations.base import RestBaseOperations


class SettingsOperations(RestBaseOperations):
    PATH = "/api/platform/settings"

    def get_all(self) -> list[dict]:
        """GET /api/platform/settings."""
        return self._client.get(self._url(self.PATH))

    def get_by_name(self, name: str) -> dict:
        """GET /api/platform/settings/{name}."""
        return self._client.get(self._url(f"{self.PATH}/{name}"))

    def get_by_module_id(self, module_id: str) -> list[dict]:
        """GET /api/platform/settings/modules/{moduleId}."""
        return self._client.get(self._url(f"{self.PATH}/modules/{module_id}"))

    def get_ui_customization(self) -> dict:
        """GET /api/platform/settings/ui/customization."""
        return self._client.get(self._url(f"{self.PATH}/ui/customization"))

    def update(self, settings: list[dict]) -> None:
        """POST /api/platform/settings — bulk update settings."""
        self._client.post(self._url(self.PATH), json=settings)
