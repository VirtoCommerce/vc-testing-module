import allure
import pytest
import requests
import datetime


@pytest.fixture(scope="session")
@allure.title("Fixture to obtain the bearer token")
def auth_token(config):
    url = f"{config['base_url']}/connect/token"
    data = {
        "grant_type": "password",
        "username": config["username"],
        "password": config["password"],
    }
    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
    }

    print(data)

    response = requests.post(url, data=data, headers=headers)
    response.raise_for_status()

    local_storage_auth = response.json()
    expires_in = local_storage_auth.pop("expires_in", 0)
    expires_at = datetime.datetime.utcnow() + datetime.timedelta(seconds=expires_in)
    expires_at = expires_at.strftime("%Y-%m-%dT%H:%M:%S.") + f"{expires_at.microsecond // 1000:03d}Z"
    local_storage_auth["expires_at"] = expires_at

    return response.json()["access_token"], local_storage_auth
