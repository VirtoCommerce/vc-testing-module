from playwright.sync_api import Page


class SuccessfulRegistrationPage:
    def __init__(self, config: dict, page: Page):
        self.page = page
        self.config = config

    @property
    def url(self) -> str:
        return f"{self.config['frontend_base_url']}/successful-registration"
