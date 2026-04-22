from playwright.sync_api import Locator


class FilterFacetComponent:
    def __init__(self, element: Locator):
        self.element = element

    @property
    def facet_items(self) -> list[Locator]:
        return self.element.locator(".vc-menu-item").all()

    def click_header(self) -> None:
        self.element.locator(".vc-widget__header-container").click()

    def click_facet_item(self, id: str) -> None:
        facet_item = next(
            (item for item in self.facet_items if item.get_attribute("data-test-id") == id),
            None,
        )
        if facet_item:
            facet_item.click()
