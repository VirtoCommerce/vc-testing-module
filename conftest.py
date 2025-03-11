import os
from dotenv import load_dotenv
import allure
import pytest
import requests
import datetime
from gql import Client, gql
from gql.transport.requests import RequestsHTTPTransport
from playwright.sync_api import sync_playwright, expect
from e2e.graphql import client
from fixtures.auth_token import auth_token
from fixtures.graphql_client import graphql_client
from fixtures.authenticated_page import authenticated_page
from fixtures.clear_cart_if_not_empty import clear_cart_if_not_empty

# Load environment variables from .env file
load_dotenv()


# Define a fixture for global variables
@pytest.fixture(scope="session")
def config():
    return {
        "base_url": os.getenv("BASE_URL", "https://vcst-qa-storefront.govirto.com"),
        "username": os.getenv("USER_EMAIL", "b2badmin@test.com"),
        "password": os.getenv("PASSWORD", "Password1"),
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
def user_context(graphql_client, config):
    user = client.get_me(graphql_client, "")
    return user


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
