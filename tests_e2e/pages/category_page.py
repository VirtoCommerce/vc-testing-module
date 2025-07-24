from tests_e2e.pages.main_layout_page import MainLayoutPage
from playwright.sync_api import Locator, Page
from tests_e2e.components.category_view_switcher_component import CategoryViewSwitcherComponent
from tests_e2e.components.product_card_component import ProductCardComponent
from typing import List, Optional


class CategoryPage(MainLayoutPage):
    def __init__(self, config: dict, page: Page, seo_path: str):
        self.config = config
        self.page = page
        self.seo_path = seo_path

    @property
    def url(self) -> str:
        return f"{self.config['frontend_base_url']}/{self.seo_path}"

    @property
    def view_switcher(self) -> CategoryViewSwitcherComponent:
        return CategoryViewSwitcherComponent(self.page.locator("[data-test-id='category-page.view-switcher']"))

    @property
    def products_grid_view(self) -> Locator:
        return self.page.locator("[data-test-id='category-page.products-grid-view']")

    @property
    def products_list_view(self) -> Locator:
        return self.page.locator("[data-test-id='category-page.products-list-view']")

    @property
    def product_cards(self) -> List[ProductCardComponent]:
        return [ProductCardComponent(card) for card in self.products_grid_view.locator("[data-test-id='product-card']").all()]

    def navigate(self) -> None:
        self.page.goto(self.url)
        self.page.wait_for_load_state("networkidle")

    def get_product_card_by_sku(self, sku: str) -> Optional[ProductCardComponent]:
        for product_card in self.product_cards:
            if product_card.sku == sku:
                return product_card
        return None
