from .login_locators import LoginLocators
from utils.video_freeze import video_freeze
from utils.swiper_freeze import swiper_freeze


class LoginPage:
    def __init__(self, page, config):
        self.page = page
        self.config = config
        self.locators = LoginLocators()

    def navigate(self):
        """Navigate to login page and prepare it for visual testing"""
        self.page.goto(self.config["base_url"])
        self.page.reload()
        self.page.wait_for_load_state("networkidle")
        self._freeze_animations()

    def _freeze_animations(self):
        """Freeze video and swiper for consistent screenshots"""
        video_freeze(self.page)
        swiper_freeze(self.page, self.locators.SWIPER)

    def click_registration_button(self):
        """Click on the registration button"""
        self.page.locator(self.locators.REGISTER_LINK).click()
