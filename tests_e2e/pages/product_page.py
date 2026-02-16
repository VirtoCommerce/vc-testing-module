from playwright.sync_api import Locator, Page

from fixtures import Config
from tests_e2e.components.variation_selector_component import VariationSelectorComponent

from .main_layout_page import MainLayoutPage


class ProductPage(MainLayoutPage):

    def __init__(self, page: Page, config: Config, seo_path: str):
        super().__init__(page)
        self.config = config
        self.seo_path = seo_path

    @property
    def url(self) -> str:
        return f"{self.config['FRONTEND_BASE_URL']}/{self.seo_path}"

    @property
    def content(self) -> Locator:
        return self.page.locator("[data-test-id='content']")

    @property
    def sidebar(self) -> Locator:
        return self.page.locator("[data-test-id='sidebar']")

    @property
    def product_name(self) -> Locator:
        return self.page.locator("h1")

    @property
    def product_price(self) -> Locator:
        return self.sidebar.locator(".product-price__value")

    @property
    def variation_selector_element(self) -> Locator:
        return self.content.locator("[data-test-id^='variant-picker-group--']").first

    @property
    def variation_selector(self) -> VariationSelectorComponent:
        return VariationSelectorComponent(self.content)

    @property
    def quantity_stepper_input(self) -> Locator:
        return self.page.locator("[data-test-id='quantity-stepper-input']")

    @property
    def quantity_stepper_decrement(self) -> Locator:
        return self.page.locator("[data-test-id='quantity-stepper-decrement']")

    @property
    def quantity_stepper_increment(self) -> Locator:
        return self.page.locator("[data-test-id='quantity-stepper-increment']")

    @property
    def count_in_cart_label(self) -> Locator:
        return self.page.locator("[data-test-id='count-in-cart-label']")

    @property
    def add_to_cart_button(self) -> Locator:
        return self.quantity_stepper_increment

    @property
    def stock_status(self) -> Locator:
        return self.sidebar.locator("[title='In stock']")

    @property
    def disabled_add_to_cart_button(self) -> Locator:
        return self.sidebar.locator("button.product-price__disabled-button")

    def navigate(self) -> None:
        self.page.goto(self.url)
        self.page.wait_for_load_state("networkidle")

    def get_current_price(self) -> str | None:
        if self.product_price.is_visible():
            return self.product_price.text_content()
        return None

    def is_add_to_cart_enabled(self) -> bool:
        return self.quantity_stepper_increment.is_visible() and self.quantity_stepper_increment.is_enabled()

    def is_variation_selector_visible(self) -> bool:
        return self.variation_selector_element.is_visible()
