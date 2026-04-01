from playwright.sync_api import Locator

from page_objects.components.component import Component


class SliderFilter(Component):
    @property
    def header(self) -> Locator:
        return self._root.locator(".vc-widget__header-container")

    @property
    def content(self) -> Locator:
        return self._root.locator(".vc-widget__slot-container")

    @property
    def start_input(self) -> Locator:
        return self._root.locator("[data-test-id='slider-input-start']")

    @property
    def end_input(self) -> Locator:
        return self._root.locator("[data-test-id='slider-input-end']")
