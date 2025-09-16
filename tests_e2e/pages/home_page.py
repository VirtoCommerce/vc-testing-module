from playwright.sync_api import Page

from .main_layout_page import MainLayoutPage


class HomePage(MainLayoutPage):
    def __init__(self, page: Page, config: dict):
        self.page = page
        self.config = config

    @property
    def url(self) -> str:
        return f"{self.config['frontend_base_url']}/"

    def navigate(self):
        self.page.goto(self.url)
        self.page.wait_for_load_state("networkidle")
