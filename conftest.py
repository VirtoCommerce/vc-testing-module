import datetime
import os

import allure
import pytest
import requests
from dotenv import load_dotenv
from gql import Client, gql
from gql.transport.requests import RequestsHTTPTransport

# from fixtures.clear_cart_if_not_empty import clear_cart_if_not_empty
# from graphql_requests.queries.me.me_query import MeQuery
from playwright.sync_api import expect, sync_playwright

from fixtures.anonymous_catalog_requests_fixture import anonymous_catalog_requests
from fixtures.auth_fixture import auth

# from graphql_requests.queries.me.me_query import MeQuery
from fixtures.auth_token import auth_token
from fixtures.authenticated_page import authenticated_page
from fixtures.dataset_fixture import dataset
from fixtures.graphql_client_fixture import graphql_client
from fixtures.requests_tracker_fixture import requests_tracker
from fixtures.webapi_client_fixture import webapi_client

load_dotenv(override=True)


@pytest.fixture(scope="session")
def config():
    return {
        "backend_base_url": os.getenv(
            "BACKEND_BASE_URL", "https://vcst-qa.govirto.com"
        ),
        "frontend_base_url": os.getenv(
            "FRONTEND_BASE_URL", "https://vcst-qa-storefront.govirto.com"
        ),
        "admin_username": os.getenv("ADMIN_USERNAME"),
        "admin_password": os.getenv("ADMIN_PASSWORD"),
        "store_id": os.getenv("STORE_ID"),
        "users_password": os.getenv("USERS_PASSWORD"),
    }


def pytest_addoption(parser):

    parser.addoption(
        "--show-browser",
        action="store_true",
        default=False,
        help="Run browser in headed mode",
    )


@pytest.fixture(scope="session")
def browser_context_args():

    return {
        "viewport": {
            "width": 1440,
            "height": 900,
        }
    }


@pytest.fixture(scope="session")
def browser_type_launch_args(pytestconfig):

    return {"headless": not pytestconfig.getoption("--show-browser")}


expect.set_options(timeout=30_000)


@pytest.fixture(scope="session")
@allure.title("Fixture to initialize browser context")
def browser_context(browser, auth_token, config):
    context = browser.new_context()
    yield context
    context.close()


# @pytest.fixture(scope="session")
# @allure.title("Fixture to initialize user context")
# def user_context(graphql_client, config):
#    get_me_request = MeQuery(graphql_client)
#    result = get_me_request.execute(user_id="")  # Pass empty string as default
#    return result["me"]


@pytest.fixture(scope="function")
@allure.title("Playwright fixture with authentication")
def authenticated_page(auth_token, config, browser_context):
    # Set auth token in headers
    browser_context.set_extra_http_headers({"Authorization": f"Bearer {auth_token[0]}"})

    # Set auth object in localStorage
    page = browser_context.new_page()
    page.goto(
        config["frontend_base_url"]
    )  # Wait for page load before manipulating storage
    page.evaluate(
        f"""
        localStorage.setItem('auth', JSON.stringify({auth_token[1]}));
        """
    )
    yield page
    page.close()
