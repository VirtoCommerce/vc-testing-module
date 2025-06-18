class LoginLocators:
    """Locators for the login page"""

    EMAIL_INPUT = "//input[@aria-label='Email']"
    PASSWORD_INPUT = "//input[@aria-label='Password']"
    LOGIN_BUTTON = "//button[@type='submit']"
    SIGN_IN_TOP = "(//a[@class='top-header-link'])[2]"
    ACCOUNT_ICON = "//span[@class='font-bold']"
    LOGOUT_BUTTON = "//button[@title='Logout']"
    VALIDATION_ERROR = ".vc-form__error-message"
