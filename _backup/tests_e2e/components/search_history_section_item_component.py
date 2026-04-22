from playwright.sync_api import Locator


class SearchHistorySectionItemComponent:
    def __init__(self, element: Locator):
        self.element = element

    @property
    def text(self) -> str | None:
        return self.element.locator(".search-dropdown__text").text_content()

    @property
    def highlighted_text(self) -> str | None:
        return self.element.locator(".search-dropdown__text [data-test-id]='highlighted-text'").text_content()
