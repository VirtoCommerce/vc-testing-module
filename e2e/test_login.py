import pytest
from playwright.sync_api import Page
from e2e.pages.login_page import LoginPage
from e2e.pages.testData.test_data import SIGNUP_ERROR


@pytest.fixture
def login_page(page: Page, config, browser_context):
    return LoginPage(page, config, browser_context)



def test_successful_login(login_page: LoginPage, config):
    """Test successful login with valid credentials"""
    login_page.navigate()
    login_page.expect_form_elements_visible()
    login_page.login(config["front_admin"], config["password"])
    login_page.expect_successful_login()


def test_invalid_credentials(login_page: LoginPage):
    """Test login with invalid credentials"""
    login_page.navigate()
    login_page.login("invalid@example.com", "wrongpassword")
    login_page.expect_validation_error(SIGNUP_ERROR["login_failed"])


def test_empty_fields_validation(login_page: LoginPage):
    """Test form validation for empty fields"""
    login_page.navigate()
    login_page.login("", "")
    login_page.expect_validation_message(SIGNUP_ERROR["required_field"], "email")
    login_page.expect_validation_message(SIGNUP_ERROR["required_field"], "password")
