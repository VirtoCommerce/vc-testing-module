from playwright.sync_api import Page, expect
from e2e.pages.locators.cart_locators import CartLocators


class CartPage:
    def __init__(self, page: Page, config: dict):
        self.page = page
        self.config = config

    def navigate(self):
        """Navigate to the cart page"""
        self.page.goto(f"{self.config['base_url']}/cart")             
        self.page.wait_for_load_state("networkidle")

    def add_product_to_cart(self, product_name: str, quantity: int):
        """Add a product to cart with specified quantity"""
        self.page.goto(f"{self.config['base_url']}/{product_name}")
        self.page.fill(CartLocators.QUANTITY_INPUT, str(quantity))
        self.page.click(CartLocators.ADD_TO_CART_BUTTON)

    def get_cart_count(self, quantity: int) -> int:
        """Get the current cart count from the menu"""
        cart_count_element = self.page.locator(CartLocators.CART_COUNT.format(str(quantity)))
        return int(cart_count_element.text_content().strip("()"))

    def expect_cart_count(self, expected_count: int, quantity: int):
        """Expect the cart count to be a specific number"""
        expect(self.page.locator(CartLocators.CART_COUNT.format(str(quantity)))).to_have_text(str(expected_count))

    def expect_product_in_cart(self, product_name: str):
        """Expect a product to be in the cart with specific quantity"""
        product_row = self.page.locator(CartLocators.CART_ITEM)
        product_name_element = self.page.locator(CartLocators.PRODUCT_TITLE.format(product_name))
        expect(product_row).to_be_visible()
        expect(product_name_element).to_be_visible()
    

    def expect_line_item_total(self, price: float, quantity: int):
        """Expect the line item total to be price * quantity"""
        product_row = self.page.locator(CartLocators.CART_ITEM)
        expected_total = price * quantity
        actual_price = product_row.locator(CartLocators.PRICE_ACTUAL).text_content()
        actual_amount = float(actual_price.replace('$', ''))
        assert abs(actual_amount - expected_total) < 0.01, f"Expected total {expected_total}, but got {actual_amount}"
        
    def click_cart_icon(self):
        """Click on cart icon to navigate to cart page"""
        self.page.click(CartLocators.CART_ICON)
        self.page.wait_for_load_state("networkidle")
        
    def clear_cart(self):
        """Clear all items from the cart"""
        clear_button = self.page.locator(CartLocators.CLEAR_CART_BUTTON)
        button_Yes = self.page.locator(CartLocators.BUTTON_YES)
        dialog_modal = self.page.locator(CartLocators.DIALOG_MODAL)   
        if clear_button.is_visible():
            clear_button.click()
            expect(dialog_modal).to_be_visible()
            button_Yes.click()
            self.page.wait_for_load_state("networkidle")

    def expect_cart_empty(self):
        """Verify that the cart is empty"""
        empty_message = self.page.locator(CartLocators.EMPTY_CART_MESSAGE)
        expect(empty_message).to_be_visible()
        