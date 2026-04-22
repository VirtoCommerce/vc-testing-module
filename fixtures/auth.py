import base64
import json
from dataclasses import asdict, dataclass
from datetime import datetime, timedelta, timezone
from threading import Lock

import allure
import pytest
import requests
from playwright.sync_api import Page

from fixtures.config import Config


@dataclass
class TokenPayload:
    grant_type: str
    scope: str | None = None
    store_id: str | None = None
    username: str | None = None
    password: str | None = None


@dataclass
class TokenData:
    access_token: str | None = None
    refresh_token: str | None = None
    expires_in: int | None = None
    token_type: str | None = None

    def to_dict(self) -> dict[str, str]:
        data = asdict(self)
        # Convert expires_in (seconds) to expires_at (ISO date string)
        expires_in = data.pop("expires_in")
        if expires_in:
            expires_at = datetime.now(timezone.utc) + timedelta(seconds=expires_in)
            data["expires_at"] = expires_at.isoformat(timespec="milliseconds").replace("+00:00", "Z")
        else:
            data["expires_at"] = None
        return data

    def get_user_id(self) -> str | None:
        """Extract user ID from JWT access token 'sub' claim."""
        if not self.access_token:
            return None
        try:
            # JWT has 3 parts: header.payload.signature
            payload_part = self.access_token.split(".")[1]
            # Add padding if needed
            padding = 4 - len(payload_part) % 4
            if padding != 4:
                payload_part += "=" * padding
            payload = json.loads(base64.urlsafe_b64decode(payload_part))
            return payload.get("sub")
        except Exception:
            return None


class Auth:
    def __init__(self, config: Config):
        self.config = config
        self.token_data: TokenData | None = None
        self.lock = Lock()

    def get_token(self, payload: TokenPayload) -> TokenData:
        """Obtain a token via the password grant.

        Retries on transient 5xx responses (typically caused by concurrent cold-start
        calls to /connect/token under pytest-xdist). 4xx responses are treated as
        permanent (bad credentials) and raised immediately.
        """
        import time

        url = f"{self.config['BACKEND_BASE_URL']}/connect/token"

        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
        }

        last_error: Exception | None = None
        for attempt in range(3):
            response = requests.post(
                url,
                data=payload.__dict__ | {"storeId": self.config["STORE_ID"]},
                headers=headers,
            )
            if response.status_code < 500:
                response.raise_for_status()
                return TokenData(**response.json())
            last_error = requests.exceptions.HTTPError(
                f"{response.status_code} {response.reason} for {url}", response=response
            )
            time.sleep(0.3 * (2**attempt))  # 0.3s, 0.6s, 1.2s

        assert last_error is not None
        raise last_error

    def set_local_storage_user_id(self, page: Page, user_id: str) -> None:
        page.add_init_script(f"localStorage.setItem('user-id', '{user_id}')")

    def revoke_token(self, page: Page | None = None) -> None:
        url = f"{self.config['BACKEND_BASE_URL']}/revoke/token"

        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
        }

        if page:
            page.add_init_script(f"localStorage.removeItem('auth')")

        response = requests.post(url, data={}, headers=headers)
        response.raise_for_status()

    def authenticate(self, username: str, password: str, page: Page | None = None) -> None:
        with self.lock:
            payload = TokenPayload(
                grant_type="password",
                scope="offline_access",
                store_id=self.config["STORE_ID"],
                username=username,
                password=password,
            )

            self.token_data = self.get_token(payload)

            if page:
                auth_data = json.dumps(self.token_data.to_dict())
                user_id = self.token_data.get_user_id()

                page.add_init_script(
                    f"""
                    localStorage.setItem('auth', JSON.stringify({auth_data}));
                    localStorage.setItem('user-id', '{user_id}');
                """
                )

                page.goto(self.config["FRONTEND_BASE_URL"])
                page.wait_for_load_state("networkidle")

    def clear_token(self) -> None:
        with self.lock:
            self.revoke_token()
            self.token_data = TokenData()

    def get_auth_headers(self) -> dict[str, str] | None:
        with self.lock:
            if self.token_data is None:
                return None

            return {
                "Authorization": f"{self.token_data.token_type} {self.token_data.access_token}",
            }


@pytest.fixture(scope="session")
@allure.title("Fixture to handle authorization token")
def auth(config: Config) -> Auth:
    return Auth(config)
