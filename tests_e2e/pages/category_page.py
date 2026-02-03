from playwright.sync_api import Locator, Page

from fixtures import Config
from tests_e2e.components import (
    CategoryViewSwitcherComponent,
    FilterFacetComponent,
    FilterSliderComponent,
    ProductCardComponent,
)

from .main_layout_page import MainLayoutPage


class CategoryPage(MainLayoutPage):
    def __init__(
        self,
        config: Config,
        page: Page,
        seo_path: str,
    ):
        self.config = config
        self.page = page
        self.seo_path = seo_path

    def _fetch_all_product_cards(self, scroll_pause_ms: int = 500):
        prev_count = 1

        while True:
            cards = self.products_grid_view.locator("[data-test-id='product-card']")
            current_count = cards.count()

            if current_count == prev_count:
                break

            prev_count = current_count

            self.page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
            self.page.wait_for_timeout(scroll_pause_ms)

            try:
                self.page.wait_for_load_state("networkidle", timeout=3000)
            except:
                pass

    @property
    def url(self) -> str:
        return f"{self.config['FRONTEND_BASE_URL']}/{self.seo_path}"

    @property
    def view_switcher(self) -> CategoryViewSwitcherComponent:
        return CategoryViewSwitcherComponent(
            self.page.locator("[data-test-id='category-page.view-switcher']")
        )

    @property
    def products_grid_view(self) -> Locator:
        return self.page.locator("[data-test-id='category-page.products-grid-view']")

    @property
    def products_list_view(self) -> Locator:
        return self.page.locator("[data-test-id='category-page.products-list-view']")

    @property
    def product_cards(self) -> list[ProductCardComponent]:
        self._fetch_all_product_cards()

        return [
            ProductCardComponent(card)
            for card in self.products_grid_view.locator(
                "[data-test-id='product-card']"
            ).all()
        ]

    @property
    def price_filter_slider(self) -> FilterSliderComponent | None:
        return FilterSliderComponent(self.page.locator("[data-test-id='filter-price']"))

    @property
    def price_filter_facets(self) -> FilterFacetComponent | None:
        return FilterFacetComponent(self.page.locator("[data-test-id='filter-price']"))

    @property
    def products_count_locator(self) -> Locator:
        return self.page.locator("[data-test-id='category-page.total-products-count']")

    def navigate(self) -> None:
        self.page.goto(f"{self.url}?sort=price-ascending")
        self.page.wait_for_load_state("networkidle")

    def get_product_card_by_sku(self, sku: str) -> ProductCardComponent | None:
        for product_card in self.product_cards:
            if product_card.sku == sku:
                return product_card
        return None
