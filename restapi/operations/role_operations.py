"""REST API operations for VirtoCommerce platform roles and permissions."""

from typing import Any

from restapi.operations.base import RestBaseOperations
from restapi.types import Role


class RoleOperations(RestBaseOperations):
    PATH = "/api/platform/security/roles"

    def create(
        self, *, name: str, description: str = "", permissions: list[dict] | None = None, **overrides: Any
    ) -> Role:
        """PUT /api/platform/security/roles → returns {succeeded}, then GET by name for the full object."""
        payload: dict[str, Any] = {
            "name": name,
            "description": description,
            "permissions": permissions or [],
            **overrides,
        }
        self._client.put(self._url(self.PATH), json=payload)
        return self.get_by_name(name)

    def get_by_name(self, role_name: str) -> Role:
        """GET /api/platform/security/roles/{roleName}."""
        response = self._client.get(self._url(f"{self.PATH}/{role_name}"))
        return Role.model_validate(response)

    def search(self, *, keyword: str | None = None, skip: int = 0, take: int = 20, **extra: Any) -> dict:
        """POST /api/platform/security/roles/search."""
        payload: dict[str, Any] = {"skip": skip, "take": take, **extra}
        if keyword is not None:
            payload["keyword"] = keyword
        return self._client.post(self._url(f"{self.PATH}/search"), json=payload)

    def update(self, role: Role, **overrides: Any) -> dict:
        """PUT /api/platform/security/roles."""
        existing = role.model_dump(by_alias=True, exclude_none=True)
        payload = {**existing, **overrides}
        return self._client.put(self._url(self.PATH), json=payload)

    def delete(self, role_id: str) -> None:
        """DELETE /api/platform/security/roles?ids={id}."""
        self._client.delete(self._url(self.PATH), params={"ids": [role_id]})

    def get_all_permissions(self) -> list[dict]:
        """GET /api/platform/security/permissions."""
        return self._client.get(self._url("/api/platform/security/permissions"))
