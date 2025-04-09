import os
from dotenv import load_dotenv
import pytest
from playwright.sync_api import expect
import allure
from graphql_requests.queries.me.me_query import MeQuery
from fixtures.auth_token import auth_token
from fixtures.graphql_client import graphql_client

# Load environment variables from .env file
load_dotenv()


@pytest.fixture(scope="session")
def config():
    """Fixture that loads test configuration from environment variables"""
    return {
        "base_url": os.getenv("BASE_URL"),
        "store_id": os.getenv("STORE_ID"),
        "username": os.getenv("USER_EMAIL"),
        "password": os.getenv("PASSWORD"),
        "back_url": os.getenv("BACK_URL", "https://vcst-qa.govirto.com"),
        "api_key": os.getenv("API_KEY", "ec15f69d-fbf0-4117-b40b-286819c164fb"),
    }


# Define the browser context configuration
@pytest.fixture(scope="session")
def browser_context_args():
    return {
        "viewport": {
            "width": 1440,
            "height": 900,
        }
    }


expect.set_options(timeout=30_000)


@pytest.fixture(scope="session")
@allure.title("Fixture to initialize browser context")
def browser_context(browser, auth_token, config):
    context = browser.new_context()
    yield context
    context.close()


@pytest.fixture(scope="session")
@allure.title("Fixture to initialize user context")
def user_context(graphql_client, auth_token, config):
    get_me_request = MeQuery(graphql_client)
    result = get_me_request.execute(user_id="")
    return result["me"]


@pytest.fixture(scope="function")
@allure.title("Playwright fixture with authentication")
def authenticated_page(auth_token, config, browser_context):

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
