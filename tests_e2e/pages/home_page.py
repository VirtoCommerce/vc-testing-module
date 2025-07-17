from playwright.sync_api import Page
from tests_e2e.components.header_component import HeaderComponent


class HomePage:
    def __init__(self, page: Page, config: dict):
        self.page = page
        self.config = config
        self.header_component = HeaderComponent(page, config)

    @property
    def url(self) -> str:
        return f"{self.config['frontend_base_url']}/"

    def navigate(self):
        self.page.goto(self.config["frontend_base_url"])
        self.page.wait_for_load_state("networkidle")
