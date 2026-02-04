from playwright.sync_api import Locator, Page

from fixtures import Config
from tests_e2e.components import AddToCartComponent
from tests_e2e.components.variation_selector_component import VariationSelectorComponent

from .main_layout_page import MainLayoutPage


class ProductPage(MainLayoutPage):
    """Page object for product detail page with B2C variation selector support."""

    def __init__(self, page: Page, config: Config, seo_path: str):
        super().__init__(page)
        self.config = config
        self.seo_path = seo_path

    @property
    def url(self) -> str:
        return f"{self.config['FRONTEND_BASE_URL']}/{self.seo_path}"

    @property
    def product_name(self) -> Locator:
        return self.page.locator("[data-test-id='product-page.product-name']")

    @property
    def product_sku(self) -> Locator:
        return self.page.locator("[data-test-id='product-page.product-sku']")

    @property
    def product_price(self) -> Locator:
        return self.page.locator("[data-test-id='product-page.product-price']")

    @property
    def stock_status(self) -> Locator:
        return self.page.locator("[data-test-id='product-page.stock-status']")

    @property
    def variation_selector_element(self) -> Locator:
        return self.page.locator("[data-test-id='product-page.variation-selector']")

    @property
    def variation_selector(self) -> VariationSelectorComponent:
        return VariationSelectorComponent(self.variation_selector_element)

    @property
    def add_to_cart_component(self) -> AddToCartComponent:
        return AddToCartComponent(self.page.locator("[data-test-id='add-to-cart-component']"))

    @property
    def add_to_cart_button(self) -> Locator:
        return self.page.locator("[data-test-id='add-to-cart-button']")

    @property
    def validation_message(self) -> Locator:
        return self.page.locator("[data-test-id='product-page.validation-message']")

    def navigate(self) -> None:
        self.page.goto(self.url)
        self.page.wait_for_load_state("networkidle")

    def get_current_sku(self) -> str | None:
        return self.product_sku.text_content()

    def get_current_price(self) -> str | None:
        return self.product_price.text_content()

    def is_add_to_cart_enabled(self) -> bool:
        return self.add_to_cart_button.is_enabled()

    def is_variation_selector_visible(self) -> bool:
        return self.variation_selector_element.is_visible()
