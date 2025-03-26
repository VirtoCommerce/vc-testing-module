from playwright.sync_api import Page, expect

class LogoutPage:
    def __init__(self, page: Page, config: dict):
        self.page = page
        self.config = config
        
    def logout(self):
        """Perform logout action"""
        self.page.locator("//button[contains(@class,'flex cursor-pointer')]").click()
        self.page.locator("//button[@title='Logout']").click()
        self.page.wait_for_load_state("networkidle")
        
    def expect_logged_out(self):
        """Verify user is logged out"""
        # Verify login button is visible (indicating logged out state)
        login_button = self.page.locator("(//a[@class='top-header-link'])[2]")
        expect(login_button).to_be_visible()
        expect(login_button).to_have_text("Sign in")