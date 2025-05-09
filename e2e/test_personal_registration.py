import pytest
from playwright.sync_api import Page, BrowserContext
from e2e.pages.signup_page import RegistrationPage
from e2e.pages.testData.user_data import get_random_user, generate_random_email
from e2e.pages.testData.test_data import SIGNUP_ERROR
from e2e.pages.locators.signup_locators import SignupLocators
from e2e.pages.login_page import LoginPage

@pytest.fixture(autouse=True)
def clear_cookies(browser_context: BrowserContext):
    """Clear all cookies before each test"""
    browser_context.clear_cookies()
    yield

@pytest.fixture
def registration_page(page: Page, config, browser_context: BrowserContext):
    return RegistrationPage(page, config, browser_context)

@pytest.fixture
def login_page(page: Page, config, browser_context: BrowserContext):
    return LoginPage(page, config, browser_context)


def test_personal_registration(registration_page: RegistrationPage, login_page: LoginPage):
    """
    Test case for personal registration:
    1. Open registration form
    2. Select personal account
    3. Fill in registration details
    4. Submit form
    5. Verify success message
    6. Navigate to home page
    7. Login with the same email and password
    8. Verify email verification error message
    """
    # Get random user data
    user = get_random_user()
    email = generate_random_email()    
    print(f"Email: {email}, Password: {user['password']}")

    # Navigate to signup page
    registration_page.navigate()
  
    # Select personal account and check required fields
    registration_page.select_personal_account()
    registration_page.validate_required_fields()
    assert len(registration_page.get_all_error_texts()) == 5, "Expected 5 required field error messages"

    # Fill in registration form   
    registration_page.clear_registration_form(
        fields=[
            SignupLocators.FIRST_NAME_INPUT,
            SignupLocators.LAST_NAME_INPUT,
            SignupLocators.EMAIL_INPUT,
            SignupLocators.PASSWORD_INPUT,
            SignupLocators.CONFIRM_PASSWORD_INPUT
        ]
    )
    registration_page.fill_personal_registration_form(
        first_name=user["first_name"],
        last_name=user["last_name"],
        email=email,
        password=user["password"],
        confirm_password=user["password"]
    )

    assert len(registration_page.get_all_error_texts()) == 0, "Expected no error messages"
    
    # Click sign up button
    registration_page.click_sign_up()
    
    # Verify success message
    assert registration_page.is_success_message_visible(), "Registration failed"
    
    # Click home page button
    registration_page.click_home_page()
    login_page.click_sign_in_link()
    login_page.login(email, user["password"])
    login_page.expect_validation_error(SIGNUP_ERROR["email_verification"])
    print("Registration successful")    