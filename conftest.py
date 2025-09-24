import datetime
import os

import allure
import pytest
from dotenv import load_dotenv
from playwright.sync_api import expect, sync_playwright
from pytest import Parser

from fixtures.anonymous_catalog_requests import anonymous_catalog_requests
from fixtures.auth import auth
from fixtures.auth_token import auth_token
from fixtures.authenticated_page import authenticated_page
from fixtures.checkout_mode import checkout_mode
from fixtures.config import config
from fixtures.dataset import dataset
from fixtures.graphql_client import graphql_client
from fixtures.product_quantity_control import product_quantity_control
from fixtures.requests_tracker import requests_tracker
from fixtures.webapi_client import webapi_client

load_dotenv(override=True)


@pytest.fixture(scope="session")
def config():
    return {
        "backend_base_url": os.getenv(
            "BACKEND_BASE_URL", "https://vcptcore-demo.govirto.com"
        ),
        "frontend_base_url": os.getenv(
            "FRONTEND_BASE_URL", "https://vcptcore-demo-storefront.govirto.com"
        ),
        "admin_username": os.getenv("ADMIN_USERNAME"),
        "admin_password": os.getenv("ADMIN_PASSWORD"),
        "store_id": os.getenv("STORE_ID"),
        "users_password": os.getenv("USERS_PASSWORD"),
    }


def pytest_addoption(parser: Parser):
    parser.addoption(
        "--checkout-mode",
        action="store",
        choices=["single-page", "multi-step"],
        default="single-page",
        help="Select checkout flow to test (e.g., single-page, multi-step)",
    )
    parser.addoption(
        "--product-quantity-control",
        action="store",
        choices=["stepper", "button"],
        default="stepper",
        help="Choose quantity selector (e.g., stepper, button)",
    )
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
