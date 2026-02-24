import os

import allure
import pytest
from dotenv import load_dotenv
from playwright.sync_api import Page, expect
from pytest import Parser

from fixtures import (
    auth,
    config,
    dataset,
    graphql_client,
    requests_tracker,
    webapi_client,
)
from fixtures.config import Config

load_dotenv(override=True)

FEATURE_MARKERS = {
    "checkout_mode": "CHECKOUT_MODE",
    "quantity_control": "PRODUCT_QUANTITY_CONTROL",
    "range_filter": "RANGE_FILTER_TYPE",
}

_config_instance = None


def _get_config():
    global _config_instance
    if _config_instance is None:
        _config_instance = Config()
    return _config_instance


def pytest_runtest_setup(item):
    cfg = _get_config()
    for marker_name, config_key in FEATURE_MARKERS.items():
        marker = item.get_closest_marker(marker_name)
        if marker:
            required_value = marker.args[0]
            actual_value = cfg[config_key]
            if actual_value != required_value:
                pytest.skip(f"Requires {marker_name}={required_value}, got {actual_value}")


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


def pytest_addoption(parser: Parser):
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
    page.goto(config["frontend_base_url"])  # Wait for page load before manipulating storage
    page.evaluate(
        f"""
        localStorage.setItem('auth', JSON.stringify({auth_token[1]}));
        """
    )
    yield page
    page.close()
