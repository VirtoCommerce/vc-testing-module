from dataclasses import dataclass
from threading import Lock
from typing import Optional, Dict
import allure, pytest, requests


@dataclass
class TokenPayload:
    grant_type: str
    scope: Optional[str] = None
    store_id: Optional[str] = None
    username: Optional[str] = None
    password: Optional[str] = None


@dataclass
class TokenData:
    access_token: Optional[str] = None
    refresh_token: Optional[str] = None
    expires_in: Optional[int] = None
    token_type: Optional[str] = None


@pytest.fixture(scope="session")
@allure.title("Fixture to handle authorization token")
def auth(config):
    class Auth:
        def __init__(self):
            self.token_data: Optional[TokenData] = None
            self.lock = Lock()

        def get_token(self, payload: TokenPayload) -> TokenData:
            url = f"{config['backend_base_url']}/connect/token"

            headers = {
                "Content-Type": "application/x-www-form-urlencoded",
            }

            response = requests.post(url, data=payload.__dict__ | {"storeId": config["store_id"]}, headers=headers)
            response.raise_for_status()

            response_data = response.json()

            return TokenData(**response_data)

        def revoke_token(self) -> None:
            url = f"{config['backend_base_url']}/revoke/token"

            headers = {
                "Content-Type": "application/x-www-form-urlencoded",
            }

            response = requests.post(url, data={}, headers=headers)
            response.raise_for_status()

        def authenticate(self, username: str, password: str) -> None:
            with self.lock:
                payload = TokenPayload(
                    grant_type="password",
                    scope="offline_access",
                    store_id=config["store_id"],
                    username=username,
                    password=password,
                )

                self.token_data = self.get_token(payload)

        def clear_token(self) -> None:
            with self.lock:
                self.revoke_token()
                self.token_data = TokenData()

        def get_auth_headers(self) -> Optional[Dict[str, str]]:
            with self.lock:
                if self.token_data is None:
                    return

                return {
                    "Authorization": f"{self.token_data.token_type} {self.token_data.access_token}",
                }

    return Auth()
