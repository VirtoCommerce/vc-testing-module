"""REST API operations for VirtoCommerce platform users."""

from typing import Any

from restapi.operations.base import RestBaseOperations


class UserOperations(RestBaseOperations):
    PATH = "/api/platform/security/users"

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
        return self._client.post(self._url(f"{self.PATH}/create"), json=payload)

    def search(self, *, search_phrase: str, take: int = 20, **extra: Any) -> dict:
        payload: dict[str, Any] = {
            "searchPhrase": search_phrase,
            "deepSearch": True,
            "sort": "memberType:asc;name:asc",
            "take": take,
            **extra,
        }
        return self._client.post(self._url(f"{self.PATH}/search"), json=payload)

    def get_by_name(self, user_name: str) -> dict:
        return self._client.get(self._url(f"{self.PATH}/{user_name}"))

    def update(self, user: dict, **overrides: Any) -> dict:
        payload = {**user, **overrides}
        return self._client.put(self._url(self.PATH), json=payload)

    def delete(self, *user_names: str) -> dict:
        return self._client.delete(self._url(self.PATH), params={"names": list(user_names)})

    def lock(self, user_id: str) -> None:
        self._client.post(self._url(f"{self.PATH}/{user_id}/lock"), json={})

    def unlock(self, user_id: str) -> None:
        self._client.post(self._url(f"{self.PATH}/{user_id}/unlock"), json={})

    def reset_password(self, user_name: str, new_password: str) -> dict:
        """POST /api/platform/security/users/{userName}/resetpassword."""
        return self._client.post(
            self._url(f"{self.PATH}/{user_name}/resetpassword"),
            json={"newPassword": new_password, "forcePasswordChangeOnNextSignIn": False},
        )

    def change_password(self, user_name: str, old_password: str, new_password: str) -> dict:
        return self._client.post(
            self._url(f"{self.PATH}/{user_name}/changepassword"),
            json={"oldPassword": old_password, "newPassword": new_password},
        )

    def validate_password(self, password: str) -> dict:
        return self._client.post(
            self._url("/api/platform/security/validatepassword"),
            json=password,
        )

    def send_verification_email(self, user_id: str) -> None:
        self._client.post(self._url(f"{self.PATH}/{user_id}/sendVerificationEmail"), json={})
