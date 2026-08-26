from playwright.sync_api import Locator

from .component import Component
from .product_configuration_option import ProductConfigurationOption

_COLLAPSED_CLASS = "vc-widget--collapsed"


class ProductConfigurationSection(Component):
    @property
    def _header(self) -> Locator:
        return self.root.locator(".vc-widget__header-container")

    @property
    def name(self) -> str | None:
        title = self.root.locator("[data-test-id='section-title']").text_content()
        return title.replace("*", "").strip() if title else title

    @property
    def selected_option_name(self) -> str | None:
        return self.root.locator("[data-test-id='section-subtitle']").text_content()

    @property
    def is_required(self) -> bool:
        return self.root.locator(".product-configuration__required").count() > 0

    @property
    def options(self) -> Locator:
        return self.root.locator("[data-test-id='product-option']")

    def is_expanded(self) -> bool:
        classes = self.root.get_attribute("class") or ""
        return _COLLAPSED_CLASS not in classes

    def expand(self) -> None:
        if not self.is_expanded():
            self._header.click()

    def collapse(self) -> None:
        if self.is_expanded():
            self._header.click()

    def find_option_by_name(self, name: str) -> ProductConfigurationOption:
        return ProductConfigurationOption(
            root=self.options.filter(has=self.root.page.locator("a", has_text=name)).first
        )

    def select_option(self, name: str) -> ProductConfigurationOption:
        self.expand()
        option = self.find_option_by_name(name=name)
        option.select()
        return option
