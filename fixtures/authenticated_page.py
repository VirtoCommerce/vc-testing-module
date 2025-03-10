import allure
import pytest


@pytest.fixture(scope="function")
@allure.title("Fixture with authentication")
def authenticated_page(auth_token, config, browser_context):
    # First add authorization token as a header
    browser_context.set_extra_http_headers({"Authorization": f"Bearer {auth_token[0]}"})

    # Initialize the page and add auth value to the local storage ( it is needed as a temporary workaround for a bug )
    # So the page won't throw user to the sign in page
    page = browser_context.new_page()
    page.goto(config["base_url"])  # Ensure the page is loaded for local storage manipulation
    page.evaluate(
        f"""
            localStorage.setItem('auth', JSON.stringify({auth_token[1]}));
        """
    )
    yield page
    page.close()
