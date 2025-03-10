from .registration_locators import RegistrationLocators
from utils.swiper_freeze import swiper_freeze


class RegistrationPage:
    def __init__(self, page, config):
        self.page = page
        self.config = config
        self.locators = RegistrationLocators()

    def navigate_to_registration_public(self):
        """Navigate to public sector registration page"""
        self.page.goto(f"{self.config['base_url']}/sign-up?sector=public")
        self.page.wait_for_load_state("networkidle")

    def _freeze_animations(self):
        """Freeze video and carousel for consistent screenshots"""
        swiper_freeze(self.page, self.locators.CAROUSEL)

    def click_private_sector_button(self):
        """Click on the private sector button"""
        self.page.locator(self.locators.PRIVATE_SECTOR_BUTTON).click()

    def click_nonprofit_sector_button(self):
        """Click on the nonprofit sector button"""
        self.page.locator(self.locators.NONPROFIT_SECTOR_BUTTON).click()
