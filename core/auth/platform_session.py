import threading
from typing import Any, Final
from urllib.parse import urlparse

import requests
from pydantic import SecretStr

from core.auth.errors import AuthenticationError
from core.global_settings import global_settings


class PlatformSession:
    _LOGIN_PATH: Final = "/api/platform/security/login"
    _IDENTITY_COOKIE: Final = ".VirtoCommerce.Identity.Application"

    def __init__(self, base_url: str) -> None:
        self._base_url = base_url.rstrip("/")
        self._lock = threading.RLock()
        self._cookies: list[dict[str, Any]] = []
        self._user_name: str | None = None

    @property
    def base_url(self) -> str:
        return self._base_url

    @property
    def user_name(self) -> str | None:
        with self._lock:
            return self._user_name

    @property
    def is_authenticated(self) -> bool:
        with self._lock:
            return bool(self._cookies)

    @property
    def cookies(self) -> list[dict[str, Any]]:
        with self._lock:
            if not self._cookies:
                raise AuthenticationError("Not authenticated. Call sign_in() first.")
            return [dict(cookie) for cookie in self._cookies]

    def storage_state(self) -> dict[str, Any]:
        return {"cookies": self.cookies, "origins": []}

    def sign_in(self, username: str, password: SecretStr) -> None:
        response = requests.post(
            url=f"{self._base_url}{self._LOGIN_PATH}",
            json={"userName": username, "password": password.get_secret_value()},
            timeout=global_settings.requests_timeout,
            verify=global_settings.verify_ssl,
        )
        try:
            response.raise_for_status()
        except requests.HTTPError as exc:
            raise requests.HTTPError(
                f"{response.status_code} POST {self._LOGIN_PATH}: {response.text}",
                response=response,
            ) from exc

        body = response.json() if response.content else {}
        if not isinstance(body, dict) or not body.get("succeeded"):
            raise AuthenticationError(
                f"POST {self._LOGIN_PATH} answered {response.status_code} for user "
                f"{username!r} but did not sign in: {body}"
            )

        value = response.cookies.get(self._IDENTITY_COOKIE)
        if not value:
            raise AuthenticationError(
                f"Sign-in for {username!r} succeeded but no {self._IDENTITY_COOKIE!r} "
                f"cookie was returned; got {sorted(response.cookies.keys())}"
            )

        parsed = urlparse(self._base_url)
        with self._lock:
            self._user_name = username
            self._cookies = [
                {
                    "name": self._IDENTITY_COOKIE,
                    "value": value,
                    "domain": parsed.hostname or "",
                    "path": "/",
                    "expires": -1,
                    "httpOnly": True,
                    "secure": parsed.scheme == "https",
                    "sameSite": "Lax",
                }
            ]

    def sign_out(self) -> None:
        with self._lock:
            self._cookies = []
            self._user_name = None
