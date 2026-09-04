from typing import Final

from playwright.sync_api import Locator, Page

NOTIFICATION_ROOT: Final = ".vc-notification"
_SUCCESS: Final = ".vc-notification--success"
_ERROR: Final = ".vc-notification--error"


class Notifications:
    def __init__(self, page: Page) -> None:
        self._page = page

    @property
    def all(self) -> Locator:
        return self._page.locator(NOTIFICATION_ROOT)

    @property
    def success(self) -> Locator:
        return self._page.locator(_SUCCESS)

    @property
    def error(self) -> Locator:
        return self._page.locator(_ERROR)

    def wait_for_success(self, text: str | None = None) -> Locator:
        target = self.success if text is None else self.success.filter(has_text=text)
        target.first.wait_for(state="visible")
        return target.first

    def wait_until_dismissed(self, timeout: float | None = None) -> None:
        self.all.first.wait_for(state="detached", timeout=timeout)
