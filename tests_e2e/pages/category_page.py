from typing import List, Literal, Optional

from playwright.sync_api import Locator, Page

from tests_e2e.components import CategoryViewSwitcherComponent, ProductCardComponent

from .main_layout_page import MainLayoutPage

from test_data.test_category import TEST_CATEGORY_1




class CategoryPage(MainLayoutPage):
    def __init__(self, config: dict, page: Page, seo_path: str):
        self.config = config
        self.page = page
        self.seo_path = seo_path

    @property
    def url(self) -> str:
        #return f"{self.config['frontend_base_url']}/{self.seo_path}"
        return f"{self.config['frontend_base_url']}/{TEST_CATEGORY_1['seoPath']}"

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
    def product_cards(self) -> List[ProductCardComponent]:
        return [
            ProductCardComponent(card)
            for card in self.products_grid_view.locator(
                ProductCardComponent.PRODUCT_CARD_COMPONENT
            ).all()
        ]

    def navigate(self) -> None:
        self.page.goto(self.url)
        self.page.wait_for_load_state("load")
        # Wait for product cards to be visible (increased timeout for CI)
        self.page.wait_for_selector(ProductCardComponent.PRODUCT_CARD_COMPONENT, state="visible", timeout=60000)

    def get_product_card_by_sku(self, sku: str) -> Optional[ProductCardComponent]:
        for product_card in self.product_cards:
            if product_card.sku == sku:
                # Ensure the card is scrolled into view so nested controls are interactable
                product_card.element.scroll_into_view_if_needed()
                return product_card
        return None

    def get_first_product_card(self) -> Optional[ProductCardComponent]:
        """Returns the first product card found on the page."""
        product_cards = self.product_cards
        if product_cards:
            first_card = product_cards[0]
            # Ensure the card is scrolled into view so nested controls are interactable
            first_card.element.scroll_into_view_if_needed()
            return first_card
        return None
