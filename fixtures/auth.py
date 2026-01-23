import json
from dataclasses import asdict, dataclass
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
        data["expires_at"] = data.pop("expires_in")

        return data


class Auth:
    def __init__(self, config: Config):
        self.config = config
        self.token_data: TokenData | None = None
        self.lock = Lock()

    def get_token(self, payload: TokenPayload) -> TokenData:
        url = f"{self.config['BACKEND_BASE_URL']}/connect/token"

        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
        }

        response = requests.post(
            url,
            data=payload.__dict__ | {"storeId": self.config["STORE_ID"]},
            headers=headers,
        )

        response.raise_for_status()

        response_data = response.json()

        return TokenData(**response_data)

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

    def authenticate(
        self, username: str, password: str, page: Page | None = None
    ) -> None:
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
                page.add_init_script(
                    f"localStorage.setItem('auth', JSON.stringify({self.token_data.to_dict()}))"
                )

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
