import allure
import datetime
import pytest
import requests


@pytest.fixture(scope="session")
@allure.title("Fixture to dynamically obtain and return bearer token")
def auth_token(config) -> str:
    token_data = {"token": None, "expires_at": None}

    if token_data["token"] and token_data["expires_at"]:
        current_time = datetime.datetime.now(datetime.timezone.utc)
        if current_time < token_data["expires_at"]:
            return token_data["token"]

    url = f"{config['base_url']}/connect/token"

    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
    }

    data = {
        "grant_type": "password",
        "scope": "offline_access",
        "storeId": config["store_id"],
        "username": config["username"],
        "password": config["password"],
    }

    response = requests.post(url, data=data, headers=headers)
    response.raise_for_status()

    response_data = response.json()
    expires_in = response_data.get("expires_in", 0)
    expires_at = datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(seconds=expires_in)

    token_data["token"] = response_data["access_token"]
    token_data["expires_at"] = expires_at

    return token_data["token"]
