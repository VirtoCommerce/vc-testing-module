import pytest
from playwright.sync_api import Page, BrowserContext
from e2e.pages.signup_page import RegistrationPage
from e2e.pages.testData.user_data import get_random_user, PASSWORD_TEST_CASES, generate_valid_password, generate_random_email
from e2e.pages.testData.test_data import SIGNUP_ERROR

@pytest.fixture(autouse=True)
def clear_cookies(browser_context: BrowserContext):
    """Clear all cookies before each test"""
    browser_context.clear_cookies()
    yield

@pytest.fixture
def registration_page(page: Page, config, browser_context: BrowserContext):
    return RegistrationPage(page, config, browser_context)

def test_company_registration(registration_page: RegistrationPage):
    """
    Test case for company registration:
    1. Open registration form
    2. Select organization type
    3. Fill in registration details
    4. Submit form
    5. Verify success message
    6. Navigate to home page
    """
    # Get random user data
    user = get_random_user()
    print(f"User: {user}")
    
    # Navigate to signup page
    registration_page.navigate()
  
    # Select organization type
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
    print(f"User: {user}")
    
    # Navigate to signup page
    registration_page.navigate()
    registration_page.select_company_account()
    
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
        registration_page.clear_registration_form()
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
        registration_page.navigate()
        registration_page.select_company_account()

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
                
        registration_page.clear_registration_form()
        registration_page.fill_registration_form(
            first_name=user["first_name"],
            last_name=user["last_name"],
            email=user["email"],
            organization_name=user["company_name"],
            password=password,
            confirm_password=password
        )
        
        registration_page.click_sign_up_button()
        
        # Verify error message   
        assert registration_page.is_password_error_visible(), f"No error shown for invalid password: {case}"
        error_messages = registration_page.get_all_password_error_texts()
        print(f"Error messages: {error_messages}")      
        
        # Verify specific error messages
        if case == "no_lowercase":
            assert registration_page.get_password_error_text().lower().find("lowercase") != -1, "Missing lowercase error message"
        elif case == "no_uppercase":
            assert registration_page.get_password_error_text().lower().find("uppercase") != -1, "Missing uppercase error message"
        elif case == "too_short":
            assert registration_page.get_password_error_text().lower().find("8 characters") != -1, "Missing length error message"        
        elif case == "no_numbers":
            assert registration_page.get_password_error_text().lower().find("number") != -1, "Missing number error message"
        
       
       

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
        
        registration_page.clear_registration_form()
        registration_page.fill_registration_form(
            first_name=user["first_name"],
            last_name=user["last_name"],
            email=user["email"],
            organization_name=user["company_name"],
            password=case["password"],
            confirm_password=case["confirm_password"]
        )
        
        # Click sign up button
        registration_page.click_sign_up_button()
        
        # Verify error messages
        assert registration_page.is_password_error_visible(), f"No error shown for mismatched passwords: {case['description']}"
        
        # Get all error messages
        error_texts = registration_page.get_all_password_error_texts()
        print(f"Found error messages: {error_texts}")
        
        # Verify all expected error messages are present
        for expected_error in case["expected_errors"]:
            assert any(expected_error in error_text for error_text in error_texts), \
                f"Expected error message '{expected_error}' not found in {error_texts}"
    