import pytest
from playwright.sync_api import Page, BrowserContext
from e2e.pages.signup_page import RegistrationPage
from e2e.pages.testData.user_data import get_random_user, PASSWORD_TEST_CASES, generate_valid_password, generate_random_email
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

def test_company_registration(registration_page: RegistrationPage, login_page: LoginPage):
    """
    Test case for company registration:
    1. Open registration form
    2. Select company account
    3. Fill in registration details
    4. Submit form
    5. Verify success message
    6. Navigate to home page
    """
    # Get random user data
    user = get_random_user()
    email = user["email"]
    print(f"Email: {email}, Password: {user['password']}")
    
    # Navigate to signup page
    registration_page.navigate()
  
    # Select company account
    registration_page.select_company_account()
    
    # Fill in registration form
    registration_page.fill_registration_form(
        first_name=user["first_name"],
        last_name=user["last_name"],
        email=user["email"],
        organization_name=user.get("company_name", f"{user['first_name']} Company"),
        password=user["password"],
        confirm_password=user["confirm_password"]
    )
    
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

def test_valid_password_combinations(registration_page: RegistrationPage):
    """
    Test various valid password combinations:
    1. Test multiple valid passwords
    2. Verify successful registration
    3. Verify no error messages
    """
    # Get random user data
    user = get_random_user()
    print(f"Email: {user['email']}, Password: {user['password']}")  
   
    # Test multiple valid passwords
    valid_passwords = [
        generate_valid_password(),  # Random valid password
        "Test123!@#",  # Standard valid password
        "Complex1@Pass",  # More complex valid password
        "Secure2#Word",  # Another valid combination
        "Valid3$Pass"   # Another valid combination
    ]
    
    for password in valid_passwords:
        print(f"\nTesting valid password: {password}")
        # Generate new user data with unique email for each test
        test_user = get_random_user()
        registration_page.navigate()
        registration_page.select_company_account()
        registration_page.clear_registration_form(
            fields=[
                SignupLocators.FIRST_NAME_INPUT,
                SignupLocators.LAST_NAME_INPUT,
                SignupLocators.EMAIL_INPUT,
                SignupLocators.ORGANIZATION_NAME_INPUT,
                SignupLocators.PASSWORD_INPUT,
                SignupLocators.CONFIRM_PASSWORD_INPUT
            ]
        )
        registration_page.fill_registration_form(
            first_name=test_user["first_name"],
            last_name=test_user["last_name"],
            email=test_user["email"],    
            organization_name=test_user["company_name"],
            password=password,
            confirm_password=password
        )
        
        registration_page.click_sign_up()
        
        # Verify success
        assert registration_page.is_success_message_visible(), f"Valid password '{password}' was rejected"
        
        # Navigate back for next test
        registration_page.click_home_page()
             

def test_invalid_password_combinations(registration_page: RegistrationPage):
    """
    Test various invalid password combinations:
    1. Missing required character types
    2. Too short passwords
    3. Invalid character combinations
    """
    user = get_random_user()
    
    # Navigate to signup page
    registration_page.navigate()
    registration_page.select_company_account()
    
    # Test each invalid password case
    for case, password in PASSWORD_TEST_CASES.items():
        if case == "valid":
            continue  # Skip valid password case
            
        print(f"\nTesting invalid password case: {case}")
        print(f"Password: {password}")
                
        registration_page.clear_registration_form(
            fields=[
                SignupLocators.FIRST_NAME_INPUT,
                SignupLocators.LAST_NAME_INPUT,
                SignupLocators.EMAIL_INPUT,
                SignupLocators.ORGANIZATION_NAME_INPUT,
                SignupLocators.PASSWORD_INPUT,
                SignupLocators.CONFIRM_PASSWORD_INPUT
            ]
        )
        registration_page.fill_registration_form(
            first_name=user["first_name"],
            last_name=user["last_name"],
            email=user["email"],
            organization_name=user["company_name"],
            password=password,
            confirm_password=password
        )
        
        registration_page.validate_required_fields()
        
        # Verify error message   
        assert registration_page.is_error_visible(), f"No error shown for invalid password: {case}"
        error_messages = registration_page.get_all_error_texts()
        print(f"Error messages: {error_messages}")    
              
        # Check for expected error messages based on the test case
        if case == "no_lowercase":
            assert SIGNUP_ERROR["password_lowercase"] in error_messages, \
                f"Expected lowercase error not found in {error_messages}"
        elif case == "no_uppercase":
            assert SIGNUP_ERROR["password_uppercase"] in error_messages, \
                f"Expected uppercase error not found in {error_messages}"
        elif case == "too_short":
            assert SIGNUP_ERROR["password_length"] in error_messages, \
                f"Expected length error not found in {error_messages}"
        elif case == "no_numbers":
            assert SIGNUP_ERROR["password_number"] in error_messages, \
                f"Expected number error not found in {error_messages}"
        elif case == "no_special":
            assert SIGNUP_ERROR["password_special"] in error_messages, \
                f"Expected special char error not found in {error_messages}"
        elif case == "all_lowercase":
            assert SIGNUP_ERROR["password_uppercase"] in error_messages, \
                f"Expected lowercase error not found in {error_messages}"
        elif case == "all_uppercase":
            assert SIGNUP_ERROR["password_lowercase"] in error_messages, \
                f"Expected uppercase error not found in {error_messages}"        
        elif case == "all_special":
            assert SIGNUP_ERROR["password_uppercase"] in error_messages, \
                f"Expected special char error not found in {error_messages}"
        elif case == "random_invalid_1":
            assert registration_page.is_error_visible(), \
                f"Expected invalid password error not found in {error_messages}"
        elif case == "random_invalid_2":
            assert registration_page.is_error_visible(), \
                f"Expected invalid password error not found in {error_messages}"
        elif case == "random_invalid_3":
            assert registration_page.is_error_visible(), \
                f"Expected invalid password error not found in {error_messages}"
        

def test_password_mismatch(registration_page: RegistrationPage):
    """
    Test password confirmation validation:
    1. Password and confirm password must match
    2. Both fields must be filled
    """
    user = get_random_user()
    
    # Navigate to signup page
    registration_page.navigate()
    registration_page.select_company_account()
    
    # Test cases for password mismatch
    test_cases = [
        {
            "password": "Test123!@#",
            "confirm_password": "Test123!@$",
            "description": "Different special characters",
            "expected_errors": [SIGNUP_ERROR["password_match"]]
        },
        {
            "password": "Test123!@#",
            "confirm_password": "test123!@#",
            "description": "Different case",
            "expected_errors": [SIGNUP_ERROR["password_match"]]
        },
        {
            "password": "Test123!@#",
            "confirm_password": "",
            "description": "Empty confirm password",
            "expected_errors": [SIGNUP_ERROR["password_match"]]
        },
        {
            "password": "",
            "confirm_password": "Test123!@#",
            "description": "Empty password",
            "expected_errors": [SIGNUP_ERROR["password_required"], SIGNUP_ERROR["password_match"]]
        }
    ]
    
    for case in test_cases:
        print(f"\nTesting password mismatch: {case['description']}")
        
        registration_page.clear_registration_form(
            fields=[
                SignupLocators.FIRST_NAME_INPUT,
                SignupLocators.LAST_NAME_INPUT,
                SignupLocators.EMAIL_INPUT,
                SignupLocators.ORGANIZATION_NAME_INPUT,
                SignupLocators.PASSWORD_INPUT,
                SignupLocators.CONFIRM_PASSWORD_INPUT
            ]
        )
        registration_page.fill_registration_form(
            first_name=user["first_name"],
            last_name=user["last_name"],
            email=user["email"],
            organization_name=user["company_name"],
            password=case["password"],
            confirm_password=case["confirm_password"]
        )
        
        # Click sign up button
        registration_page.validate_required_fields()
        
        # Verify error messages
        assert registration_page.is_error_visible(), f"No error shown for mismatched passwords: {case['description']}"
        
        # Get all error messages
        error_texts = registration_page.get_all_error_texts()
        print(f"Found error messages: {error_texts}")
        
        # Verify all expected error messages are present
        for expected_error in case["expected_errors"]:
            assert any(expected_error in error_text for error_text in error_texts), \
                f"Expected error message '{expected_error}' not found in {error_texts}"
            

def test_valid_email_formats(registration_page: RegistrationPage):
    """
    Test various valid email formats during registration:
    1. Test standard email format
    2. Test email with dot in local part
    3. Test email with plus sign
    4. Test email with subdomain
    5. Verify no error messages for valid formats
    """
    user = get_random_user() 
        
    # Test cases for valid email formats
    valid_emails = [
        {
            "email": "test@example.com",
            "description": "Standard email"
        },
        {
            "email": "test.name@example.com",
            "description": "Email with dot"
        },
        {
            "email": "test+label@example.com",
            "description": "Email with plus sign"
        },
        {
            "email": "test@sub.example.com",
            "description": "Email with subdomain"
        }
    ]
    
    for case in valid_emails:
        print(f"\nTesting valid email format: {case['description']}")
        print(f"Email: {case['email']}")
        registration_page.navigate()
        registration_page.select_company_account()
        registration_page.clear_registration_form(
            fields=[
                SignupLocators.FIRST_NAME_INPUT,
                SignupLocators.LAST_NAME_INPUT,
                SignupLocators.EMAIL_INPUT,
                SignupLocators.ORGANIZATION_NAME_INPUT,
                SignupLocators.PASSWORD_INPUT,
                SignupLocators.CONFIRM_PASSWORD_INPUT
            ]
        )
        registration_page.fill_registration_form(
            first_name=user["first_name"],
            last_name=user["last_name"],
            email=case["email"],
            organization_name=user["company_name"],
            password=user["password"],
            confirm_password=user["confirm_password"]
        )
        
        registration_page.click_sign_up()
        
        # Verify no error message for valid email
        assert not registration_page.is_error_visible(), \
            f"Error shown for valid email: {case['email']}"

def test_invalid_email_formats(registration_page: RegistrationPage, config):
    """
    Test various invalid email formats during registration:
    1. Test missing @ symbol
    2. Test missing local part
    3. Test missing domain
    4. Test invalid domain format
    5. Test empty email
    6. Test double dot in domain
    7. Verify appropriate error messages
    8. Verify email duplicate error message
    """
    user = get_random_user() 

    # Navigate to signup page
    registration_page.navigate()
    registration_page.select_company_account()  
    
    # Test cases for invalid email formats
    invalid_emails = [
        {
            "email": "invalid.email",
            "description": "Missing @ symbol",
            "expected_error": SIGNUP_ERROR["email_invalid"]
        },
        {
            "email": "@example.com",
            "description": "Missing local part",
            "expected_error": SIGNUP_ERROR["email_invalid"]
        },
        {
            "email": "test@",
            "description": "Missing domain",
            "expected_error": SIGNUP_ERROR["email_invalid"]
        },
        {
            "email": "test@.com",
            "description": "Invalid domain",
            "expected_error": SIGNUP_ERROR["email_invalid"]
        },
        {
            "email": "",
            "description": "Empty email",
            "expected_error": SIGNUP_ERROR["required_field"]
        },
        {
            "email": "test@example..com",
            "description": "Double dot in domain",
            "expected_error": SIGNUP_ERROR["email_invalid"]
        },
        {
            "email": config["username"],
            "description": "Email already exists",
            "expected_error": SIGNUP_ERROR["email_duplicate"]
        }
    ]
    
    for case in invalid_emails:
        print(f"\nTesting invalid email format: {case['description']}")
        print(f"Email: {case['email']}")    
        registration_page.clear_registration_form(
            fields=[
                SignupLocators.FIRST_NAME_INPUT,
                SignupLocators.LAST_NAME_INPUT,
                SignupLocators.EMAIL_INPUT,
                SignupLocators.ORGANIZATION_NAME_INPUT,
                SignupLocators.PASSWORD_INPUT,
                SignupLocators.CONFIRM_PASSWORD_INPUT
            ]
        )
        registration_page.fill_registration_form(
            first_name=user["first_name"],
            last_name=user["last_name"],
            email=case["email"],
            organization_name=user["company_name"],
            password=user["password"],
            confirm_password=user["confirm_password"]
        )
        
        registration_page.validate_required_fields()
        
        # Verify error message is shown
        assert registration_page.is_error_visible(), \
            f"No error shown for invalid email: {case['email']}"
        
        error_text = registration_page.get_all_error_texts()
        print(f"Error message: {error_text}")
        
        # Verify specific error message
        assert case["expected_error"] in error_text, \
            f"Expected error message containing '{case['expected_error']}' not found in {error_text}"
    
    