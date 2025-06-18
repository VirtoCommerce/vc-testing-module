import os
from dotenv import load_dotenv
import pytest
import requests
import datetime
from gql import Client, gql
from gql.transport.requests import RequestsHTTPTransport
from playwright.sync_api import sync_playwright, expect
from fixtures.auth_token import auth_token
from fixtures.authenticated_page import authenticated_page

# from fixtures.clear_cart_if_not_empty import clear_cart_if_not_empty
# from graphql_requests.queries.me.me_query import MeQuery
from playwright.sync_api import expect
import allure

# from graphql_requests.queries.me.me_query import MeQuery
from fixtures.auth_token import auth_token
from fixtures.graphql_client import graphql_client
from fixtures.user_service import user_service

# Load environment variables from .env file
load_dotenv()


@pytest.fixture(scope="session")
def config():
    """Fixture that loads test configuration from environment variables"""
    return {
        "base_url": os.getenv("BASE_URL", "https://vcst-qa-storefront.govirto.com"),
        "store_id": os.getenv("STORE_ID"),
        "username": os.getenv("USER_EMAIL"),
        "front_admin": os.getenv("FRONT_ADMIN"),
        "password": os.getenv("PASSWORD"),
        "back_url": os.getenv("BACK_URL", "https://vcst-qa.govirto.com"),
        "api_key": os.getenv("API_KEY", "ec15f69d-fbf0-4117-b40b-286819c164fb"),
    }


def pytest_addoption(parser):

    parser.addoption("--show-browser", action="store_true", default=False, help="Run browser in headed mode")


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
    page.goto(config["base_url"])  # Wait for page load before manipulating storage
    page.evaluate(
        f"""
        localStorage.setItem('auth', JSON.stringify({auth_token[1]}));
        """
    )
    yield page
    page.close()


# ========================================
# CONVENIENCE FUNCTIONS FOR MULTI-BROWSER TESTING
# ========================================
@pytest.fixture(scope="function")
@allure.title("Function to get browser information")
def get_browser_info(page):
    """Get detailed browser information for reporting"""
    browser = page.context.browser
    browser_name = browser.browser_type.name
    version = browser.version
    
    # Get additional browser context info
    viewport = page.viewport_size
    user_agent = page.evaluate("navigator.userAgent")
    
    browser_info = {
        "browser_name": browser_name,
        "version": version,
        "viewport": viewport,
        "user_agent": user_agent,
        "url": page.url
    }
    
    return browser_info

@pytest.fixture(scope="function")
@allure.title("Function to take a screenshot")
def take_login_screenshot(page, description="Login Screenshot"):
    """Take a screenshot and attach it to allure report"""
    screenshot = page.screenshot()
    browser_name = page.context.browser.browser_type.name
    
    # Create a descriptive name with browser info
    screenshot_name = f"{description}-{browser_name}"
    
    allure.attach(
        screenshot, 
        name=screenshot_name, 
        attachment_type=allure.attachment_type.PNG
    )
    
    return screenshot

@pytest.fixture(scope="function")
def validate_login_result(page, expected_success=True):
    """Validate login result and return success status"""
    current_url = page.url
    browser_name = page.context.browser.browser_type.name
    
    # Basic validation - page should be responsive
    assert current_url is not None, f"Page unresponsive on {browser_name}"
    
    # Check if we're still on login page or redirected (basic success indicator)
    is_on_login_page = "login" in current_url.lower()
    login_successful = not is_on_login_page if expected_success else is_on_login_page
    
    # Attach result to allure report
    result_info = {
        "browser": browser_name,
        "current_url": current_url,
        "login_successful": login_successful,
        "expected_success": expected_success
    }
    
    allure.attach(
        str(result_info), 
        name=f"Login-Validation-{browser_name}", 
        attachment_type=allure.attachment_type.TEXT
    )
    
    return login_successful
