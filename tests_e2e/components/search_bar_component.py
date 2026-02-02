from playwright.sync_api import Locator

from tests_e2e.components.search_suggestions_dropdown_component import (
    SearchSuggestionsDropdownComponent,
)


class SearchBarComponent:
    def __init__(self, element: Locator) -> None:
        self.element = element

    @property
    def search_input(self) -> Locator:
        return self.element.locator("[data-test-id='global-search-query-input']")

    @property
    def search_button(self) -> Locator:
        return self.element.locator("[data-test-id='global-search-apply-button']")

    @property
    def category_scope_button(self) -> Locator:
        return self.element.locator("[data-search-scope]")

    @property
    def suggestions_dropdown(self) -> SearchSuggestionsDropdownComponent:
        return SearchSuggestionsDropdownComponent(
            self.element.locator("[data-test-id='global-search-suggestions-dropdown']")
        )
