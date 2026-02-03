from playwright.sync_api import Locator, Page, expect

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

    def get_product_card_by_sku(
        self, sku: str, max_pages_count: int = 5, scroll_pause_ms: int = 500
    ) -> ProductCardComponent | None:
        for _ in range(max_pages_count):
            product_card = next(
                (
                    product_card
                    for product_card in self.product_cards
                    if product_card.sku == sku
                ),
                None,
            )
            if product_card:
                return product_card

            self.page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
            self.page.wait_for_timeout(scroll_pause_ms)
        return None
