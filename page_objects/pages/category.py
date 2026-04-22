from playwright.sync_api import Locator, Page
from playwright.sync_api import TimeoutError as PlaywrightTimeoutError

from core.global_settings import GlobalSettings
from page_objects.components.category_view_switcher import CategoryViewSwitcher
from page_objects.components.checkboxes_filter import CheckboxesFilter
from page_objects.components.product_card import ProductCard
from page_objects.components.slider_filter import SliderFilter
from page_objects.layouts.main import MainLayout


class CategoryPage(MainLayout):
    def __init__(
        self,
        global_settings: GlobalSettings,
        page: Page,
        path: str,
        sort: str = "price-ascending",
    ) -> None:
        super().__init__(global_settings=global_settings, page=page)
        self._path = path
        self._sort = sort

    @property
    def url(self) -> str:
        return f"{self._global_settings.frontend_base_url}/{self._path}?sort={self._sort}"

    @property
    def products_count_label(self) -> Locator:
        return self._page.locator("[data-test-id='products-count-label']")

    @property
    def view_switcher(self) -> CategoryViewSwitcher:
        return CategoryViewSwitcher(root=self._page.locator("[data-test-id='view-switcher']"))

    @property
    def grid_view(self) -> Locator:
        return self._page.locator("[data-test-id='products-grid-view']")

    @property
    def list_view(self) -> Locator:
        return self._page.locator("[data-test-id='products-list-view']")

    @property
    def price_slider_filter(self) -> SliderFilter:
        return SliderFilter(root=self._page.locator("[data-test-id='filter-price']"))

    @property
    def price_checkboxes_filter(self) -> CheckboxesFilter:
        return CheckboxesFilter(root=self._page.locator("[data-test-id='filter-price']"))

    def navigate(self) -> None:
        self._page.goto(url=self.url, wait_until="load")

    def scroll_to_product(self, sku: str) -> ProductCard:
        card = self._page.locator(f"[data-product-sku='{sku}']")
        all_cards = self._page.locator("[data-product-sku]")

        all_cards.first.wait_for()

        while True:
            if card.count() > 0:
                card.first.scroll_into_view_if_needed()
                return ProductCard(root=card.first)

            count_before = all_cards.count()
            self._page.evaluate("window.scrollTo(0, document.body.scrollHeight)")

            try:
                all_cards.nth(count_before).wait_for(timeout=3000)
            except PlaywrightTimeoutError:
                raise RuntimeError(f"Product with SKU '{sku}' not found on category page")
