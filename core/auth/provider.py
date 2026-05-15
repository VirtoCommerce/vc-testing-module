import threading
from typing import Final

import requests
from pydantic import SecretStr

from core.auth.token_info import TokenInfo
from core.global_settings import global_settings


class AuthProvider:
    _AUTH_TOKEN_PATH: Final = "/connect/token"

    def __init__(self, base_url: str) -> None:
        self._base_url = base_url
        self._token_info: TokenInfo | None = None
        self._lock = threading.RLock()

    @property
    def base_url(self) -> str:
        return self._base_url

    @property
    def is_authenticated(self) -> bool:
        with self._lock:
            return self._token_info is not None and not self._token_info.is_expired

    @property
    def token_info(self) -> TokenInfo | None:
        with self._lock:
            return self._token_info

    @property
    def headers(self) -> dict[str, str]:
        with self._lock:
            if self._token_info is None:
                return {"Content-Type": "application/json"}
            if self._token_info.is_expired:
                self._refresh()
            return {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self._token_info.access_token.get_secret_value()}",
            }

    def _refresh(self) -> None:
        with self._lock:
            if self._token_info is None:
                raise RuntimeError("Not authenticated. Call sign_in() first.")
            if not self._token_info.is_expired:
                return
            if self._token_info.refresh_token is None:
                raise RuntimeError(
                    "Token expired and no refresh token available. Re-authenticate."
                )
            refresh_token = self._token_info.refresh_token

        response = requests.post(
            url=f"{self._base_url}{self._AUTH_TOKEN_PATH}",
            data={"grant_type": "refresh_token", "refresh_token": refresh_token},
            timeout=global_settings.requests_timeout,
            verify=global_settings.verify_ssl,
        )
        try:
            response.raise_for_status()
        except requests.HTTPError as exc:
            raise requests.HTTPError(
                f"{response.status_code} POST {self._AUTH_TOKEN_PATH} (refresh): {response.text}",
                response=response,
            ) from exc
        with self._lock:
            self._token_info = TokenInfo.model_validate(response.json())

    def sign_in(self, username: str, password: SecretStr) -> None:
        payload = {
            "grant_type": "password",
            "scope": "offline_access",
            "username": username,
            "storeId": global_settings.store_id,
            "password": password.get_secret_value(),
        }
        response = requests.post(
            url=f"{self._base_url}{self._AUTH_TOKEN_PATH}",
            data=payload,
            timeout=global_settings.requests_timeout,
            verify=global_settings.verify_ssl,
        )
        try:
            response.raise_for_status()
        except requests.HTTPError as exc:
            raise requests.HTTPError(
                f"{response.status_code} POST {self._AUTH_TOKEN_PATH}: {response.text}",
                response=response,
            ) from exc
        with self._lock:
            self._token_info = TokenInfo.model_validate(response.json())

    def sign_out(self) -> None:
        with self._lock:
            self._token_info = None
