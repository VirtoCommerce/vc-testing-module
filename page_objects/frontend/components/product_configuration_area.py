from playwright.sync_api import Locator

from .component import Component
from page_objects.frontend.components.product_configuration_option import ProductConfigurationOption
from page_objects.frontend.components.product_configuration_section import ProductConfigurationSection


class ProductConfigurationArea(Component):
    @property
    def sections(self) -> Locator:
        return self.root.locator("[data-test-id='section']")

    def find_section_by_name(self, name: str) -> ProductConfigurationSection:
        return ProductConfigurationSection(
            root=self.sections.filter(has=self.root.page.locator("[data-test-id='section-title']", has_text=name)).first
        )

    def select_option(self, section_name: str, option_name: str) -> ProductConfigurationOption:
        return self.find_section_by_name(name=section_name).select_option(name=option_name)
