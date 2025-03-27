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

    def expect_product_in_cart(self, product_name: str, line_item_number: int):
        """Expect a product to be in the cart with specific quantity"""
        product_row = self.page.locator(CartLocators.CART_ITEM_1.format(line_item_number))
        product_name_element = self.page.locator(CartLocators.PRODUCT_TITLE.format(product_name, line_item_number))
        expect(product_row).to_be_visible()
        expect(product_name_element).to_be_visible()
    

    def get_line_items(self):
        """Get all line items in the cart"""
        return self.page.locator(CartLocators.LINE_ITEM).all()
    

    def expect_line_item_total(self, product_name: str, price: float, quantity: int, line_item_number1: int, line_item_number2: int):
        """Expect the line item total to be price * quantity for a specific product"""
        line_item = self.page.locator(CartLocators.CART_ITEM_1.format(line_item_number1))
        expect(line_item).to_be_visible()
        
        expected_total = price * quantity
        actual_price = line_item.locator(CartLocators.PRICE_ACTUAL_CART_ITEM_1.format(line_item_number2)).text_content()
        actual_amount = float(actual_price.replace('$', '').replace(',', ''))
        assert abs(actual_amount - expected_total) < 0.01, f"Expected total {expected_total} for product {product_name}, but got {actual_amount}"
        
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

    def set_quantity(self, quantity: int):
        """Set quantity for product"""
        self.page.fill("#input-1306", str(quantity))
        expect(self.page.locator("#input-1306")).to_have_value(str(quantity))

    def expect_max_quantity_error(self):
        """Verify max quantity error message"""
        error_message = self.page.locator("text=You can order maximum 20 item(s)")
        expect(error_message).to_be_visible()

    def expect_subtotal(self, amount: str):
        """Verify subtotal amount"""
        subtotal = self.page.locator(f"text=Subtotal ${amount}")
        expect(subtotal).to_be_visible()

    def proceed_to_checkout(self):
        """Click proceed to checkout button"""
        self.page.click("text=PROCEED TO CHECKOUT")
        