import time
from typing import Optional

from playwright.sync_api import Locator, Page

from tests_e2e.components import CategoryViewSwitcherComponent, ProductCardComponent

from .main_layout_page import MainLayoutPage


class CategoryPage(MainLayoutPage):
    def __init__(
        self, config: dict, page: Page, seo_path: str, product_quantity_control: str
    ):
        self.config = config
        self.page = page
        self.seo_path = seo_path
        self.product_quantity_control = product_quantity_control

    @property
    def url(self) -> str:
        return f"{self.config['frontend_base_url']}/{self.seo_path}"

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

    def navigate(self) -> None:
        self.page.goto(f"{self.url}?sort=price-ascending")
        self.page.wait_for_load_state("networkidle")

    def get_product_card_by_sku(self, sku: str) -> Optional[ProductCardComponent]:
        for product_card in self.product_cards:
            if product_card.sku == sku:
                return product_card
        return None

    def add_product_to_cart(self, sku: str, quantity: int) -> None:
        product_card = self.get_product_card_by_sku(sku)
        if product_card:
            if self.product_quantity_control == "stepper":
                for _ in range(quantity):
                    product_card.quantity_stepper_component.increment_button.click()
            elif self.product_quantity_control == "button":
                product_card.add_to_cart_component.quantity_input.fill(str(quantity))
                product_card.add_to_cart_component.add_to_cart_text_button.click()
            time.sleep(2)
