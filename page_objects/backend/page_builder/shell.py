from collections.abc import Callable
from typing import Final

from playwright.sync_api import Locator, Page

from core.global_settings import GlobalSettings
from page_objects.backend.page_builder.constants import Menu, Route
from page_objects.backend.page_builder.page_details_blade import PageDetailsBlade
from page_objects.backend.page_builder.pages_list_blade import PagesListBlade
from page_objects.backend.shell import (
    AppMenu,
    BladeNavigation,
    ConfirmationPopup,
    Notifications,
)

_BADGE: Final = ".vc-badge__text"
_LOGO: Final = ".sidebar-header__logo-image"
_USER_NAME: Final = ".vc-user-info__name"
_USER_ROLE: Final = ".vc-user-info__role"

_MENU_FOR_ROUTE: Final = {
    Route.ALL: Menu.ALL,
    Route.DRAFT: Menu.DRAFT,
    Route.PENDING: Menu.PENDING,
    Route.ACTIVE: Menu.ACTIVE,
    Route.ARCHIVED: Menu.ARCHIVED,
}


class PageBuilderShell:
    def __init__(self, page: Page, global_settings: GlobalSettings) -> None:
        self._page = page
        self._global_settings = global_settings
        self.menu = AppMenu(page)
        self.blades = BladeNavigation(page)
        self.popup = ConfirmationPopup.on(page)
        self.notifications = Notifications(page)

    def url(self, route: str = Route.ALL, store_id: str | None = None) -> str:
        return self._global_settings.page_builder_shell_url(store_id=store_id, route=route)

    def open(self, route: str = Route.ALL, store_id: str | None = None) -> None:
        target = self.url(route, store_id)
        same_document = self._page.url.split("#")[0] == target.split("#")[0]
        self._page.goto(target)
        if same_document:
            self._page.reload(wait_until="networkidle")
        else:
            self._page.wait_for_load_state("networkidle")
        self.blades.all.first.wait_for(state="visible")

    def wait_settled(self) -> None:
        self._page.wait_for_load_state("networkidle")

    def wait_for_list(self, route: str, predicate: Callable[[PagesListBlade], bool]) -> PagesListBlade:
        for attempt in range(self._global_settings.poll_attempts):
            self.open(route)
            listing = self.list_blade
            if predicate(listing):
                return listing
            if attempt < self._global_settings.poll_attempts - 1:
                self._page.wait_for_timeout(self._global_settings.poll_interval * 1000)
        return self.list_blade

    def wait_until_listed(self, route: str, name: str) -> PagesListBlade:
        return self.wait_for_list(route, lambda listing: listing.reveal(name))

    def wait_until_absent(self, route: str, name: str) -> PagesListBlade:
        return self.wait_for_list(route, lambda listing: not listing.reveal(name))

    def wait_for_counter(self, route: str, menu_id: str, expected: int) -> None:
        self.wait_for_list(route, lambda _: self.counter(menu_id) == expected)
        actual = self.counter(menu_id)
        assert actual == expected, (
            f"{menu_id} counter is {actual}, expected {expected} " f"(list shows {self.list_blade.count} rows)"
        )

    def go_to(self, route: str) -> None:
        self.menu.open(_MENU_FOR_ROUTE[route])
        self.blades.all.first.wait_for(state="visible")

    @property
    def list_blade(self) -> PagesListBlade:
        return PagesListBlade(self.blades.all.first)

    @property
    def details_blade(self) -> PageDetailsBlade:
        return PageDetailsBlade(self.blades.all.last)

    def open_page(self, name: str) -> PageDetailsBlade:
        self.list_blade.open_page(name)
        return self.details_blade.wait_until_loaded()

    def add_page(self) -> PageDetailsBlade:
        self.list_blade.add()
        return self.details_blade.wait_until_ready()

    def counter(self, menu_id: str) -> int:
        badge = self.menu.item(menu_id).locator(_BADGE)
        if badge.count() == 0:
            return 0
        text = (badge.first.inner_text() or "").strip()
        return int(text) if text.isdigit() else 0

    def stable_counter(self, menu_id: str, attempts: int = 10, interval_ms: int = 400) -> int:
        previous = self.counter(menu_id)
        for _ in range(attempts):
            self._page.wait_for_timeout(interval_ms)
            current = self.counter(menu_id)
            if current == previous:
                return current
            previous = current
        return previous

    @property
    def logo(self) -> Locator:
        return self._page.locator(_LOGO)

    @property
    def user_name(self) -> Locator:
        return self._page.locator(_USER_NAME)

    @property
    def user_role(self) -> Locator:
        return self._page.locator(_USER_ROLE)
