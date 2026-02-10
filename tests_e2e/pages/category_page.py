from playwright.sync_api import Locator, Page, TimeoutError

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
    def end_list_label(self) -> Locator:
        return self.page.locator("[data-test-id='end-list-label']")

    @property
    def products_loader(self) -> Locator:
        return self.page.locator("[data-test-id='category-products-loader']")

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

    def get_product_card_by_sku(self, sku: str) -> ProductCardComponent | None:
        return next(
            (
                product_card
                for product_card in self.product_cards
                if product_card.sku == sku
            ),
            None,
        )

    def scroll_to_product_card(
        self, sku: str, page_limit: int = 10
    ) -> ProductCardComponent | None:
        product_card_locator = self.products_grid_view.locator(
            "[data-test-id='product-card']"
        )
        for _ in range(page_limit):
            product_card = self.get_product_card_by_sku(sku)
            if product_card:
                product_card.element.scroll_into_view_if_needed()
                return product_card
            self.products_loader.or_(self.end_list_label).wait_for(state="visible")
            if self.end_list_label.is_visible():
                break
            current_count = product_card_locator.count()
            with self.page.expect_response(
                lambda response: "/graphql" in response.url
                and response.status == 200
            ):
                self.products_loader.scroll_into_view_if_needed()
            product_card_locator.nth(current_count).wait_for()
        return None
