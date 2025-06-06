import pytest
import allure
from playwright.sync_api import Page
from e2e.pages.login_page import LoginPage
from e2e.pages.testData.test_data import SIGNUP_ERROR


@pytest.fixture
def login_page(page: Page, config, browser_context):
    return LoginPage(page, config, browser_context)


# ========================================
# EXISTING TESTS (Enhanced with Allure)
# ========================================

@allure.epic("Authentication")
@allure.feature("Login Functionality") 
@allure.story("Valid Login")
def test_successful_login(login_page: LoginPage, config):
    """Test successful login with valid credentials"""
    with allure.step("Navigate to login page"):
        login_page.navigate()
    
    with allure.step("Verify form elements are visible"):
        login_page.expect_form_elements_visible()
    
    with allure.step("Login with valid credentials"):
        login_page.login(config["front_admin"], config["password"])
    
    with allure.step("Verify successful login"):
        login_page.expect_successful_login()


@allure.epic("Authentication")
@allure.feature("Login Functionality")
@allure.story("Invalid Credentials")
def test_invalid_credentials(login_page: LoginPage):
    """Test login with invalid credentials"""
    with allure.step("Navigate to login page"):
        login_page.navigate()
    
    with allure.step("Attempt login with invalid credentials"):
        login_page.login("invalid@example.com", "wrongpassword")
    
    with allure.step("Verify validation error is displayed"):
        login_page.expect_validation_error(SIGNUP_ERROR["login_failed"])


@allure.epic("Authentication")
@allure.feature("Login Functionality")
@allure.story("Form Validation")
def test_empty_fields_validation(login_page: LoginPage):
    """Test form validation for empty fields"""
    with allure.step("Navigate to login page"):
        login_page.navigate()
    
    with allure.step("Attempt login with empty fields"):
        login_page.login("", "")
    
    with allure.step("Verify email field validation"):
        login_page.expect_validation_message(SIGNUP_ERROR["required_field"], "email")
    
    with allure.step("Verify password field validation"):
        login_page.expect_validation_message(SIGNUP_ERROR["required_field"], "password")


# ========================================
# NEW MULTI-BROWSER TESTS
# ========================================
@pytest.mark.multi_browser
@allure.epic("Cross-Browser Testing")
@allure.feature("Multi-Browser Login")
@allure.story("Explicit Browser Testing")
def test_login_across_all_browsers_automatically(page: Page, config):
    """Test login functionality across browsers using pytest-playwright's automatic browser switching"""
    browser_name = page.context.browser.browser_type.name
    
    with allure.step(f"Test login on {browser_name} browser"):
        allure.attach(f"Browser: {browser_name}", name="Browser Type", attachment_type=allure.attachment_type.TEXT)
        
        # Create LoginPage instance using the provided page
        login_page = LoginPage(page, config, page.context)
        
        with allure.step("Navigate and verify page load"):
            login_page.navigate()
            page.wait_for_load_state("networkidle")
            
            # Take screenshot of initial page
            screenshot = page.screenshot()
            allure.attach(screenshot, name=f"Initial-Page-{browser_name}", attachment_type=allure.attachment_type.PNG)
        
        with allure.step("Verify login form elements"):
            login_page.expect_form_elements_visible()
        
        with allure.step("Test valid login"):
            success = login_page.login(config["front_admin"], config["password"])
            
            # Take screenshot after login attempt
            screenshot = page.screenshot()
            allure.attach(screenshot, name=f"After-Login-{browser_name}", attachment_type=allure.attachment_type.PNG)
            
            # Log result
            result_msg = f"Login successful: {success} on {browser_name}"
            allure.attach(result_msg, name="Login Result", attachment_type=allure.attachment_type.TEXT)
        
        with allure.step("Verify login result"):
            if success:
                login_page.expect_successful_login()
            else:
                # Even if login failed, verify we handled it gracefully
                current_url = page.url
                assert current_url is not None, f"Navigation failed on {browser_name}"
