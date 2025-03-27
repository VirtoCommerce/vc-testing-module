from playwright.sync_api import Page, expect
from e2e.pages.locators.cart_locators import CartLocators
import datetime


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
        all_products = self.page.locator(CartLocators.LINE_ITEM).all()
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
        self.page.wait_for_selector(CartLocators.PRICE_ACTUAL_CART_ITEM_1.format(line_item_number2), state="attached")
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
        """Set quantity for product and wait for price recalculation"""
        self.page.fill(CartLocators.QUANTITY_INPUT, str(quantity))
        expect(self.page.locator(CartLocators.QUANTITY_INPUT)).to_have_value(str(quantity))
        # Wait for price recalculation
        self.page.wait_for_load_state("networkidle")
        # Wait for the price element to be updated with a longer timeout
        self.page.wait_for_selector(CartLocators.SUBTOTAL, state="attached", timeout=10000)
        # Additional wait to ensure price is fully updated
        self.page.wait_for_timeout(2000)  # Wait 2 seconds for price recalculation

    def expect_subtotal(self, amount: float):
        """Verify subtotal amount"""
        subtotal = self.page.locator(CartLocators.SUBTOTAL)
        expect(subtotal).to_be_visible()
        # Wait for price to update
        self.page.wait_for_load_state("networkidle")
        subtotal_amount = subtotal.text_content()
        float_subtotal_amount = float(subtotal_amount.replace('$', '').replace(',', ''))
        assert abs(float_subtotal_amount - amount) < 0.01, f"Expected subtotal {amount} but got {float_subtotal_amount}"

    def proceed_to_checkout(self):
        """Click proceed to checkout button"""
        self.page.click(CartLocators.PROCEED_TO_CHECKOUT_BUTTON)

    def expect_currency(self, currency: str):
        """Verify the currency symbol in cart"""
        currency_element = self.page.locator(f"//span[contains(text(), '{currency}')]")
        expect(currency_element).to_be_visible()

    def expect_cart_not_empty(self):
        """Verify that the cart is not empty"""
        empty_message = self.page.locator(CartLocators.EMPTY_CART_MESSAGE)
        expect(empty_message).not_to_be_visible()

    def change_currency(self, currency: str):
        """Change the currency in the cart"""
        currency_selector = self.page.locator(CartLocators.CURRENCY_SELECTOR)
        currency_selector.click()
        self.page.locator(f"text={currency}").click()
        self.page.wait_for_load_state("networkidle")
    
    
    def expect_product_count(self, expected_count: int):
        """Verify and log the expected number of products in cart"""
        actual_count = self.page.locator(CartLocators.LINE_ITEM).count()
        
        print("=== Product Count Verification ===")
        print(f"Time: {datetime.datetime.now()}")
        print(f"Expected count: {expected_count}")
        print(f"Actual count: {actual_count}")
        
        if actual_count == expected_count:
            print("Status: ✅ Count matches expectation")
        else:
            print("Status: ❌ Count mismatch!")
        print("================================")
        
        assert actual_count == expected_count, f"Expected {expected_count} products in cart, but found {actual_count}"

        