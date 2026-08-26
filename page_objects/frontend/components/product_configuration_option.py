from playwright.sync_api import Locator

from .component import Component


class ProductConfigurationOption(Component):
    @property
    def _radio(self) -> Locator:
        return self.root.locator("input[type='radio']")

    @property
    def name(self) -> str | None:
        return self.root.locator("a").first.text_content()

    @property
    def product_id(self) -> str | None:
        return self._radio.get_attribute("value")

    @property
    def price(self) -> Locator:
        return self.root.locator(".vc-product-price__actual").first

    def is_selected(self) -> bool:
        return self._radio.is_checked()

    def select(self) -> None:
        self.root.locator(".vc-radio-button__container").click()
