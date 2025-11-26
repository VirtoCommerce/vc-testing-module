from playwright.sync_api import Locator


class FacetComponent:
    def __init__(self, element: Locator):
        self.element = element

    @property
    def open_button(self) -> Locator:
        return self.element.locator("[data-test-id='facet-filter-open-button']")
