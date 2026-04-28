from playwright.sync_api import Locator

from tests_e2e.components.search_products_section_item_component import (
    SearchProductsSectionItemComponent,
)


class SearchProductsSectionComponent:
    def __init__(self, element: Locator):
        self.element = element

    @property
    def title(self) -> str:
        return self.element.locator(".search-dropdown__head").text_content()

    @property
    def products_list_element(self) -> Locator:
        return self.element.locator(".search-dropdown__products")

    @property
    def products(self) -> list[SearchProductsSectionItemComponent]:
        locators = self.element.locator(".vc-product-card").all()
        return [SearchProductsSectionItemComponent(locator) for locator in locators]

    @property
    def view_all_button(self) -> Locator:
        return self.element.locator(".search-dropdown__view-all button")
