import allure
import datetime
import pytest
import requests


@pytest.fixture(scope="session")
@allure.title("Fixture to dynamically obtain and return bearer token")
def auth_token(config, request) -> str:
    # Make token_data local to the fixture
    token_data = {"token": None, "expires_at": None}

    def get_token():
        # Validate required config upfront for clearer errors
        missing = [k for k in ("store_id", "username", "password", "backend_base_url") if not config.get(k)]
        if missing:
            raise RuntimeError(f"Missing required config values for token request: {', '.join(missing)}")

        if token_data["token"] and token_data["expires_at"]:
            current_time = datetime.datetime.now(datetime.timezone.utc)
            if current_time < token_data["expires_at"]:
                return token_data["token"]

        url = f"{config['frontend_base_url']}/connect/token"

        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
        }

        data = {
            "grant_type": "password",
            "scope": config.get("scope") or "openid profile offline_access",
            "storeId": config["store_id"],
            "username": config["username"],
            "password": config["password"],
        }

        # Optionally include client credentials if provided by environment
        if config.get("client_id"):
            data["client_id"] = config["client_id"]
        if config.get("client_secret"):
            data["client_secret"] = config["client_secret"]

        response = requests.post(url, data=data, headers=headers)
        try:
            response.raise_for_status()
        except requests.HTTPError:
            try:
                allure.attach(response.text, name="/connect/token response", attachment_type=allure.attachment_type.TEXT)
            except Exception:
                pass
            raise

        response_data = response.json()
        expires_in = response_data.get("expires_in", 0)
        expires_at = datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(seconds=expires_in)

        token_data["token"] = response_data["access_token"]
        token_data["expires_at"] = expires_at

        # Build a minimal auth object for storefront localStorage
        auth_local_storage = {
            "accessToken": response_data["access_token"],
            "tokenType": response_data.get("token_type", "Bearer"),
            "expiresIn": expires_in,
            "userName": config["username"],
        }

        return token_data["token"], __import__("json").dumps(auth_local_storage)

    # Get initial token
    token = get_token()

    # Add cleanup to clear token data after tests
    def cleanup():
        token_data["token"] = None
        token_data["expires_at"] = None

    # Register cleanup using request.addfinalizer
    request.addfinalizer(cleanup)

    return token
