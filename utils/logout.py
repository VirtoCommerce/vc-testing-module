from playwright.sync_api import Page, expect
from e2e.pages.locators.top_header_locators import TopHeaderLocators
from playwright.sync_api import BrowserContext


class LogoutPage:
    def __init__(self, page: Page, config: dict, browser_context: BrowserContext):
        self.page = page
        self.config = config
        self.browser_context = browser_context

    def logout(self):
        """Perform logout action"""
        self.page.locator("//button[contains(@class,'flex cursor-pointer')]").click()
        self.page.locator("//button[@title='Logout']").click()
        self.page.wait_for_load_state("networkidle")

    def expect_logged_out(self):
        """Verify user is logged out"""
        # Verify login button is visible (indicating logged out state)
        login_button = self.page.locator(TopHeaderLocators.SIGN_IN_LINK)
        expect(login_button).to_be_visible()
        expect(login_button).to_have_text("Sign in")

    def go_to_home_page(self):
        """Go to home page"""
        self.page.click("(//nav[contains(@class,'relative z-[2]')]//a)[1]")
        self.page.wait_for_load_state("networkidle")
        self.page.wait_for_url(f"{self.config['base_url']}")
        self.page.wait_for_load_state("domcontentloaded")
