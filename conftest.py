import os

import allure
import pytest
from dotenv import load_dotenv
from playwright.sync_api import Page, expect
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


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    Capture and store the test outcome on the item so fixtures can react to failures.
    """
    outcome = yield
    rep = outcome.get_result()
    setattr(item, f"rep_{rep.when}", rep)


@pytest.fixture
def _page_for_failure(request) -> Page | None:
    """
    Ensure we can grab the Playwright page before it is closed, but only for tests that use it.
    """
    if "page" not in request.fixturenames:
        return None
    return request.getfixturevalue("page")


@pytest.fixture(autouse=True)
def screenshot_on_failure(request, _page_for_failure: Page | None):
    """
    Take a Playwright page screenshot when a test using the `page` fixture fails.
    """
    yield

    rep_call = getattr(request.node, "rep_call", None)
    if not rep_call or not rep_call.failed or _page_for_failure is None:
        return

    page = _page_for_failure

    screenshots_dir = os.path.join("screenshots", "failures")
    os.makedirs(screenshots_dir, exist_ok=True)

    screenshot_path = os.path.join(screenshots_dir, f"{request.node.name}.png")
    page.screenshot(path=screenshot_path, full_page=True)

    allure.attach.file(
        screenshot_path,
        name=request.node.name,
        attachment_type=allure.attachment_type.PNG,
    )


@pytest.fixture(scope="session")
def config():
    return {
        "backend_base_url": os.getenv(
            "BACKEND_BASE_URL"#, "https://vcptcore-demo.govirto.com"
        ),
        "frontend_base_url": os.getenv(
            "FRONTEND_BASE_URL"#, "https://vcptcore-demo-storefront.govirto.com"
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
