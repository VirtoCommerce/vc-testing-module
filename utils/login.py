from playwright.sync_api import Page


def login(page: Page, config: dict) -> None:
    """
    A utility function to log in to the application.
    It fills the email and password fields and clicks the login button.

    :param page: The Playwright Page object.
    :param config: The configuration dictionary containing credentials.
    """
    page.goto(config["base_url"])
    page.wait_for_load_state("domcontentloaded")
    page.get_by_placeholder("Enter your email address").fill(config["username"])
    page.get_by_placeholder("Enter your password").fill(config["password"])
    page.get_by_role("button", name="Log in").click()
