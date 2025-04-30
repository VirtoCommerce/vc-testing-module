import allure
import pytest
import requests
from gql import Client
from typing import Optional


@pytest.fixture(scope="session")
@allure.title("Fixture to provide user authentication service")
def user_service(config, graphql_client):
    class UserService:
        def __init__(self, base_url: str, client: Client):
            self.base_url = base_url
            self.client = client
            self._current_token: Optional[str] = None

        def sign_in(self, username: str, password: str) -> str:
            url = f"{self.base_url}/connect/token"

            headers = {
                "Content-Type": "application/x-www-form-urlencoded",
            }

            data = {
                "grant_type": "password",
                "scope": "offline_access",
                "storeId": config["store_id"],
                "username": username,
                "password": password,
            }

            response = requests.post(url, data=data, headers=headers)
            response.raise_for_status()

            response_data = response.json()
            self._current_token = response_data["access_token"]

            self.client.set_headers({"Authorization": f"Bearer {self._current_token}"})

            return self._current_token

        def sign_out(self) -> None:
            self._current_token = None
            self.client.set_headers({"Authorization": None})

        @property
        def current_token(self) -> Optional[str]:
            return self._current_token

    return UserService(config["base_url"], graphql_client)
