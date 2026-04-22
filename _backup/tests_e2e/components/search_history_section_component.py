from playwright.sync_api import Locator

from tests_e2e.components.search_history_section_item_component import (
    SearchHistorySectionItemComponent,
)


class SearchHistorySectionComponent:
    def __init__(self, element: Locator) -> None:
        self.element = element

    @property
    def title(self) -> str:
        return self.element.locator(".search-dropdown__head").text_content()

    @property
    def item_list(self) -> Locator:
        return self.element.locator(".search-dropdown__list")

    @property
    def items(self) -> list[SearchHistorySectionItemComponent]:
        locators = self.element.locator(".search-dropdown__item").all()
        return [SearchHistorySectionItemComponent(locator) for locator in locators]

    def get_item(self, text: str) -> SearchHistorySectionItemComponent | None:
        return next((item for item in self.items if item.text == text), None)

    def has_item(self, text: str) -> bool:
        return any(item.text == text for item in self.items)

    def has_highlighted_text(self, text: str) -> bool:
        return any(item.highlighted_text == text for item in self.items)
