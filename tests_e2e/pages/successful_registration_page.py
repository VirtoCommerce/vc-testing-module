from playwright.sync_api import Page

from fixtures.config import Config


class SuccessfulRegistrationPage:
    def __init__(self, config: Config, page: Page):
        self.page = page
        self.config = config

    @property
    def url(self) -> str:
        return f"{self.config['FRONTEND_BASE_URL']}/successful-registration"
