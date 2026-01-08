from playwright.sync_api import Page

from fixtures.config import Config

from .main_layout_page import MainLayoutPage


class HomePage(MainLayoutPage):
    def __init__(self, page: Page, config: Config):
        self.page = page
        self.config = config

    @property
    def url(self) -> str:
        return f"{self.config['FRONTEND_BASE_URL']}/"

    def navigate(self):
        self.page.goto(self.url)
        self.page.wait_for_load_state("networkidle")
