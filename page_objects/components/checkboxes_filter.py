from playwright.sync_api import Locator

from page_objects.components.component import Component


class CheckboxesFilter(Component):
    @property
    def header(self) -> Locator:
        return self._root.locator(".vc-widget__header-container")

    @property
    def content(self) -> Locator:
        return self._root.locator(".vc-widget__slot-container")

    def facet(self, facet_id: str) -> Locator:
        return self._root.locator(f"[data-test-id='{facet_id}']")
