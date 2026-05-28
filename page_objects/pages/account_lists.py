from playwright.sync_api import Locator

from page_objects.components.wishlist_card import WishlistCard
from page_objects.layouts.main import MainLayout


class AccountListsPage(MainLayout):
    @property
    def url(self) -> str:
        return f"{self._global_settings.frontend_base_url}/account/lists"

    @property
    def create_list_button(self) -> Locator:
        return self.root.locator("[data-test-id='create-wishlist-button']")

    @property
    def cards(self) -> Locator:
        return self._page.locator("[data-test-id='wishlist-card']")

    def find_card(self, name: str) -> WishlistCard:
        return WishlistCard(root=self.cards.filter(has_text=name).first)

    def navigate(self) -> None:
        self._page.goto(url=self.url, wait_until="load")
