from playwright.sync_api import Locator


class ChipComponent:
    def __init__(self, element: Locator):
        self.element = element

    @property
    def label(self) -> str:
        return self.element.locator(".vc-chip__content").text_content()

    @property
    def close_button(self) -> Locator:
        return self.element.locator(".vc-chip__close-button")

    def close_chip(self) -> None:
        self.close_button.click()
