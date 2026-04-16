"""REST API operations for VirtoCommerce platform roles and permissions."""

from typing import Any

from restapi.operations.base import RestBaseOperations


class RoleOperations(RestBaseOperations):
    PATH = "/api/platform/security/roles"

    def create(
        self, *, name: str, description: str = "", permissions: list[dict] | None = None, **overrides: Any
    ) -> dict:
        """POST /api/platform/security/roles."""
        payload: dict[str, Any] = {
            "name": name,
            "description": description,
            "permissions": permissions or [],
            **overrides,
        }
        return self._client.post(self._url(self.PATH), json=payload)

    def get_by_name(self, role_name: str) -> dict:
        """GET /api/platform/security/roles/{roleName}."""
        return self._client.get(self._url(f"{self.PATH}/{role_name}"))

    def search(self, *, keyword: str | None = None, skip: int = 0, take: int = 20, **extra: Any) -> dict:
        """POST /api/platform/security/roles/search."""
        payload: dict[str, Any] = {"skip": skip, "take": take, **extra}
        if keyword is not None:
            payload["keyword"] = keyword
        return self._client.post(self._url(f"{self.PATH}/search"), json=payload)

    def update(self, role: dict, **overrides: Any) -> dict:
        """PUT /api/platform/security/roles."""
        payload = {**role, **overrides}
        return self._client.put(self._url(self.PATH), json=payload)

    def delete(self, role_id: str) -> None:
        """DELETE /api/platform/security/roles?ids={id}."""
        self._client.delete(self._url(self.PATH), params={"ids": [role_id]})

    def get_all_permissions(self) -> list[dict]:
        """GET /api/platform/security/permissions."""
        return self._client.get(self._url("/api/platform/security/permissions"))
