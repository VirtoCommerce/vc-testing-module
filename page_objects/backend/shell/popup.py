from typing import Final

from playwright.sync_api import Locator, Page

from page_objects.component import Component

POPUP_ROOT: Final = ".vc-popup"
_PORTAL_ROOT: Final = "#headlessui-portal-root"


class ConfirmationPopup(Component):
    @classmethod
    def on(cls, page: Page) -> "ConfirmationPopup":
        return cls(page.locator(POPUP_ROOT))

    @property
    def panel(self) -> Locator:
        return self._root.locator(".vc-popup__panel")

    @property
    def title(self) -> Locator:
        return self._root.locator(".vc-popup__title")

    @property
    def content(self) -> Locator:
        return self._root.locator(".vc-popup__content")

    @property
    def confirm_button(self) -> Locator:
        return self._root.locator(".vc-popup__footer button", has_text="Confirm")

    @property
    def cancel_button(self) -> Locator:
        return self._root.locator(".vc-popup__footer button", has_text="Cancel")

    @property
    def close_button(self) -> Locator:
        return self._root.locator(".vc-popup__close-btn")

    @property
    def is_open(self) -> bool:
        return self._root.count() > 0

    def wait_until_open(self) -> None:
        self.panel.wait_for(state="visible")

    def confirm(self) -> None:
        self.wait_until_open()
        self.confirm_button.click()
        self._root.wait_for(state="detached")

    def cancel(self) -> None:
        self.wait_until_open()
        self.cancel_button.click()
        self._root.wait_for(state="detached")

    def close(self) -> None:
        self.wait_until_open()
        self.close_button.click()
        self._root.wait_for(state="detached")

    def dismiss_if_open(self) -> None:
        if self.is_open:
            self.cancel()
