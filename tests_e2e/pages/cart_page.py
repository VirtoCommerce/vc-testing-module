from typing import List, Optional

from playwright.sync_api import Locator, Page

from tests_e2e.components import (
    CheckoutPaymentDetailsComponent,
    CheckoutShippingDetailsComponent,
    ClearCartModalComponent,
    LineItemComponent,
)

from .main_layout_page import MainLayoutPage


class CartPage(MainLayoutPage):
    def __init__(self, config: dict, page: Page):
        self.config = config
        self.page = page

    @property
    def url(self) -> str:
        return f"{self.config['frontend_base_url']}/cart"

    @property
    def line_items(self) -> List[LineItemComponent]:
        return [
            LineItemComponent(item)
            for item in self.page.locator("[data-test-id='line-item']").all()
        ]

    @property
    def clear_cart_button(self) -> Locator:
        return self.page.locator("[data-test-id='cart.clear-button']")

    @property
    def checkout_button(self) -> Locator:
        return self.page.locator("[data-test-id='cart.checkout-button']")

    @property
    def is_empty(self) -> bool:
        return len(self.line_items) == 0

    @property
    def shipping_details_section_component(
        self,
    ) -> Optional[CheckoutShippingDetailsComponent]:
        return CheckoutShippingDetailsComponent(
            self.page.locator("[data-test-id='checkout.shipping-details-section']")
        )

    @property
    def payment_details_section_component(
        self,
    ) -> Optional[CheckoutPaymentDetailsComponent]:
        return CheckoutPaymentDetailsComponent(
            self.page.locator("[data-test-id='checkout.payment-details-section']")
        )

    @property
    def single_page_place_order_button(self) -> Locator:
        return self.page.locator(
            "[data-test-id='checkout-single-page.place-order-button']"
        )

    @property
    def place_order_button(self) -> Locator:
        return self.page.locator(
            "[data-test-id='checkout-single-page.place-order-button']"
        )

    def navigate(self) -> None:
        self.page.goto(self.url)
        self.page.wait_for_load_state("networkidle")

    def get_line_item_by_sku(self, sku: str) -> Optional[LineItemComponent]:
        for line_item in self.line_items:
            if line_item.sku == sku:
                return line_item
        return None

    def clear_cart(self) -> None:
        self.clear_cart_button.click()
        modal = ClearCartModalComponent(
            self.page.locator("[data-test-id='clear-cart-modal']")
        )
        modal.yes_button.click()
        self.page.wait_for_load_state("networkidle")
