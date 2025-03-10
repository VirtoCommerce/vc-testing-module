from utils.element_toggle_visibility import element_toggle_visibility
from tests_visual.pages.header.header_locators import HeaderLocators


class HeaderPage:
    def __init__(self, page):
        self.page = page

    def hide_vc_badge(self):
        """Hide the VC badge in the header"""
        element_toggle_visibility(self.page, HeaderLocators.VC_BADGE, hidden=True)
