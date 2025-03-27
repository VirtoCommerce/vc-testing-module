from playwright.sync_api import Page

class GoToHome:
    def __init__(self, page: Page, config: dict):
        self.page = page
        self.config = config

    def go_to_home(self):
        """Go to home page"""
        self.page.click("(//nav[contains(@class,'relative z-[2]')]//a)[1]")
        self.page.wait_for_load_state("networkidle")
        self.page.wait_for_url(f"{self.config['base_url']}")
        self.page.wait_for_load_state("domcontentloaded")

