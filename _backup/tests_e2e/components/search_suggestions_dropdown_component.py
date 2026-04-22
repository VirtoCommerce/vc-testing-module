from playwright.sync_api import Locator

from tests_e2e.components.search_history_section_component import (
    SearchHistorySectionComponent,
)
from tests_e2e.components.search_products_section_component import (
    SearchProductsSectionComponent,
)


class SearchSuggestionsDropdownComponent:
    def __init__(self, element: Locator):
        self.element = element

    @property
    def search_history_section(self) -> SearchHistorySectionComponent:
        return SearchHistorySectionComponent(self.element.locator("[data-test-id='global-search-history-sections']"))

    @property
    def product_suggestions_section(self) -> SearchProductsSectionComponent:
        return SearchProductsSectionComponent(
            self.element.locator("[data-test-id='global-search-products-suggestions']")
        )

    @property
    def not_found_section_element(self) -> Locator:
        return self.element.locator("[data-test-id='global-search-not-found']")
