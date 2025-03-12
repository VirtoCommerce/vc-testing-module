import allure
import pytest
import requests
import datetime
from gql import Client, gql
from gql.transport.requests import RequestsHTTPTransport
from playwright.sync_api import sync_playwright, expect
from e2e.graphql import client

expect.set_options(timeout=30_000)


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
    response = requests.post(url, data=data, headers=headers)
    response.raise_for_status()  # Raise error if request failed

    # Prepare auth value for local storage
    # Compute expires_at
    local_storage_auth = response.json()
    expires_in = local_storage_auth.pop("expires_in", 0)  # Remove expires_in, default to 0 if missing
    expires_at = datetime.datetime.utcnow() + datetime.timedelta(seconds=expires_in)

    # Format expires_at to match the second time format (milliseconds + 'Z' for UTC)
    expires_at = expires_at.strftime("%Y-%m-%dT%H:%M:%S.") + f"{expires_at.microsecond // 1000:03d}Z"
    local_storage_auth["expires_at"] = expires_at

    return response.json()["access_token"], local_storage_auth


@pytest.fixture(scope="session")
@allure.title("Fixture to initialize GraphQL Client")
def graphql_client(config, auth_token):
    transport = RequestsHTTPTransport(
        url=f"{config['base_url']}/graphql",
        headers={
            "Authorization": f"Bearer {auth_token[0]}",
        },
        use_json=True,
        verify=True,
    )
    client = Client(transport=transport, fetch_schema_from_transport=True)
    return client


@pytest.fixture(scope="session")
@allure.title("Fixture to initialize browser context")
def browser_context(browser, auth_token, config):
    context = browser.new_context()
    yield context
    context.close()


@pytest.fixture(scope="session")
@allure.title("Fixture to initialize user context")
def user_context(graphql_client, config):
    user = client.get_me(graphql_client, "")
    return user


@pytest.fixture(scope="function")
@allure.title("Playwright fixture with authentication")
def playwright_authenticated_page(auth_token, config, browser_context):

    # First add authorization token as a header
    browser_context.set_extra_http_headers({"Authorization": f"Bearer {auth_token[0]}"})

    # Initialize the page and add auth value to the local storage ( it is needed as a temporary workaround for a bug )
    # So the page won't throw user to the sign in page
    page = browser_context.new_page()
    page.goto(config["base_url"])  # Ensure the page is loaded for local storage manipulation
    page.evaluate(
        f"""
            localStorage.setItem('auth', JSON.stringify({auth_token[1]}));
        """
    )
    yield page
    page.close()
