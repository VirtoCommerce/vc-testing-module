from playwright.sync_api import Locator

from .component import Component


class Chip(Component):
    @property
    def text_label(self) -> Locator:
        return self._root.locator(".vc-chip__content")

    @property
    def close_button(self) -> Locator:
        return self._root.locator(".vc-chip__close-button")
