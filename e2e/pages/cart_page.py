from playwright.sync_api import Page, expect, BrowserContext
from e2e.pages.locators.cart_locators import CartLocators
import datetime
from utils.commonLocators.common_components_locators import CommonComponentsLocators

class CartPage:
    def __init__(self, page: Page, config: dict, browser_context: BrowserContext):
        self.page = page
        self.config = config
        self.browser_context = browser_context

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
        self.page.wait_for_selector(CommonComponentsLocators.VC_LOADER_OVERLAY_SPINNER, state="hidden")
        self.page.wait_for_selector(CartLocators.CART_ITEM_1.format(line_item_number), state="attached")
        product_row = self.page.locator(CartLocators.CART_ITEM_1.format(line_item_number))
        product_name_element = self.page.locator(CartLocators.PRODUCT_TITLE.format(product_name, line_item_number))        
        expect(product_row).to_be_visible()
        expect(product_name_element).to_be_visible()      
               
    
    def get_line_items(self):
        """Get all line items in the cart"""
        self.page.wait_for_selector(CommonComponentsLocators.VC_LOADER_OVERLAY_SPINNER, state="hidden")
        self.page.wait_for_selector(CartLocators.LINE_ITEM, state="attached")       
        line_items = self.page.locator(CartLocators.LINE_ITEM).all()
        for item in line_items:
            expect(item).to_be_attached()
            expect(item).to_be_visible()
        print(f"Found {len(line_items)} line items in cart")
        if len(line_items) == 0:
            print("No items found after clicking cart icon, trying direct navigation")
            self.navigate()
            self.page.wait_for_timeout(2000)
            line_items = self.get_line_items()    
        return line_items
    

    def expect_line_item_total(self, product_name: str, price: float, quantity: int, line_item_number1: int, line_item_number2: int):
        """Expect the line item total to be price * quantity for a specific product"""
        line_item = self.page.locator(CartLocators.CART_ITEM_1.format(line_item_number1))
        self.page.wait_for_selector(CartLocators.PRICE_ACTUAL_CART_ITEM_1.format(line_item_number2), state="attached")
        expect(line_item).to_be_visible()        
        expected_total = price * quantity
        actual_price = line_item.locator(CartLocators.PRICE_LIST).text_content()
        actual_amount = float(actual_price.replace('$', '').replace(',', ''))
        if abs(actual_amount - expected_total) < 0.01:
            print(f"✅ Success: Total {actual_amount} for product {product_name} matches expected {expected_total}")
        else:
            print(f"❌ Error: Expected total {expected_total} for product {product_name}, but got {actual_amount}")
        assert abs(actual_amount - expected_total) < 0.01, f"Expected total {expected_total} for product {product_name}, but got {actual_amount}"
        
    def click_cart_icon(self):
        """Click on cart icon to navigate to cart page"""
        self.page.click(CartLocators.CART_ICON) 
        self.page.wait_for_timeout(2000)
        self.page.wait_for_selector(CartLocators.CART_TITLE, state="attached")
        expect(self.page).to_have_url(f"{self.config['base_url']}/cart")
        self.page.wait_for_load_state("networkidle")
        self.page.wait_for_selector(CommonComponentsLocators.VC_LOADER_OVERLAY_SPINNER, state="hidden")
        

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
        self.page.wait_for_selector(CartLocators.PROCEED_TO_BUTTON, state="attached")
        self.page.locator(CartLocators.PROCEED_TO_BUTTON).click()
        self.page.wait_for_load_state("networkidle")
        self.page.wait_for_selector(CommonComponentsLocators.VC_LOADER_OVERLAY_SPINNER, state="hidden")
       
    

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
        self.page.wait_for_load_state("networkidle")
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
    
    def extract_currency_symbol(self) -> str:
        """Extract currency symbol from price text"""
        # Wait for price element to be visible
        currency_element = self.page.locator(CartLocators.PRICE_ACTUAL_CART_ITEM_1.format(3))
        self.page.wait_for_selector(CartLocators.PRICE_ACTUAL_CART_ITEM_1.format(3), state="attached")
        expect(currency_element).to_be_visible()
        
        # Get price text and extract symbol
        price_text = currency_element.text_content()
        if not price_text:
            raise ValueError("Price text is empty")
            
        currency_symbol = price_text[0].strip()
        if not currency_symbol:
            raise ValueError("Could not extract currency symbol")
        
        print("=== Currency Symbol Extraction ===")
        print(f"Original price text: {price_text}")
        print(f"Extracted symbol: {currency_symbol}")
        print("================================")
        
        return currency_symbol

    def unselect_all_items(self):
        """Unselect all items in the cart"""
        head_checkboxes = self.page.locator(CartLocators.HEAD_CHECKBOX)
        count = self.page.locator(CartLocators.HEAD_CHECKBOX).count()
        print(f"Found {count} elements")
        if count > 1:
            # Click each headcheckbox one by one
            for i, head_checkbox in enumerate(head_checkboxes.all()):
                try:
                    expect(head_checkbox).to_be_visible()
                    
                    # Click the headcheckbox
                    head_checkbox.click()
                    print(f"Clicked headcheckbox {i+1}/{count}")
                    
                    # Wait for any network requests to complete
                    self.page.wait_for_load_state("networkidle")
                    
                    # Verify this specific checkbox is now checked
                    expect(head_checkbox).not_to_be_checked()                 
                    
                    # Wait a moment before proceeding to the next checkbox
                    self.page.wait_for_timeout(500)
                except Exception as e:
                    print(f"Error clicking checkbox {i+1}: {str(e)}")
        else:
            # Get the single head checkbox
            head_checkbox = head_checkboxes.first
            if head_checkbox:
                expect(head_checkbox).to_be_visible()
                head_checkbox.click()
                self.page.wait_for_load_state("networkidle")
                expect(head_checkbox).not_to_be_checked()
            else:
                print("No head checkbox found")       
        
    def check_subtotal(self, expected_amount, max_attempts=3, timeout=1000):
        """Check if the subtotal is the expected amount"""
        self.page.wait_for_selector(CartLocators.SUBTOTAL, state="attached")
        subtotal = self.page.locator(CartLocators.SUBTOTAL)        
        expect(subtotal).to_be_visible()        
        
        # Try multiple times to get the correct subtotal
        for attempt in range(max_attempts):
            # Wait for network requests to complete
            self.page.wait_for_load_state("networkidle")
            self.page.wait_for_selector(CommonComponentsLocators.VC_LOADER_OVERLAY_SPINNER, state="hidden")
            self.page.wait_for_selector(CartLocators.SUBTOTAL, state="attached")           
            
            # Get the current subtotal
            subtotal_amount = subtotal.text_content()
            float_subtotal_amount = float(subtotal_amount.replace('$', '').replace(',', ''))       
            
            # Check if the subtotal is close to the expected amount
            if abs(float_subtotal_amount - expected_amount) < 0.01:
                print(f"Subtotal recalculated successfully to {float_subtotal_amount}")
                return True          
                
            # Wait before trying again
            self.page.wait_for_timeout(timeout)
            
        # If we get here, the subtotal didn't update correctly
        print(f"Warning: Subtotal did not update to {expected_amount} after {max_attempts} attempts")
        
        return False

    def select_items(self, count: int):
        """Select a specific number of items in the cart"""
        checkboxes = self.page.locator(CartLocators.ITEM_CHECKBOX).all()
        for i in range(count):
            if i < len(checkboxes):
                expect(checkboxes[i]).to_be_visible()
                checkboxes[i].click()
                self.page.wait_for_timeout(500)                
                expect(checkboxes[i]).to_be_checked()
        
        self.page.wait_for_selector(CommonComponentsLocators.VC_LOADER_OVERLAY_SPINNER, state="hidden")

    def expect_all_items_selected(self):
        """Verify that all items in the cart are selected"""
        # Get all checkboxes and verify at least one exists
        checkboxes = self.page.locator(CartLocators.ITEM_CHECKBOX).all()
        total_checkboxes = len(checkboxes)
        assert total_checkboxes > 0, "No checkboxes found in cart"
        
        # Wait for network requests and loading spinner to complete
        self.page.wait_for_load_state("networkidle")
        self.page.wait_for_selector(CommonComponentsLocators.VC_LOADER_OVERLAY_SPINNER, state="hidden")
        
        # Verify each checkbox is visible and checked
        for checkbox in checkboxes:
            expect(checkbox).to_be_visible()
            expect(checkbox).to_be_checked()
            
        print(f"Verified all {total_checkboxes} items are selected")

    def expect_all_items_unselected(self):
        """Verify that all items in the cart are unselected"""
        
        checkboxes = self.page.locator(CartLocators.ITEM_CHECKBOX).all()
        for checkbox in checkboxes:
            expect(checkbox).not_to_be_checked()

    def expect_selected_items_count(self, expected_count: int):
        """Verify the number of selected items in the cart"""
        selected_checkboxes = self.page.locator(CartLocators.CHECKED_ITEM_CHECKBOX).count()
        assert selected_checkboxes == expected_count, f"Expected {expected_count} selected items, but found {selected_checkboxes}"

    def expect_proceed_to_checkout_disabled(self):
        """Verify that the proceed to checkout button is disabled"""
        self.page.wait_for_load_state("networkidle")
        self.page.wait_for_selector(CommonComponentsLocators.VC_LOADER_OVERLAY_SPINNER, state="hidden")
        self.page.wait_for_selector(CartLocators.PROCEED_TO_BUTTON_DISABLED, state="attached")
        proceed_to_checkout_button = self.page.locator(CartLocators.PROCEED_TO_BUTTON_DISABLED)
        expect(proceed_to_checkout_button).to_be_disabled()

    def expect_proceed_to_checkout_enabled(self):
        """Verify that the proceed to checkout button is enabled"""
        self.page.wait_for_load_state("networkidle")
        self.page.wait_for_selector(CommonComponentsLocators.VC_LOADER_OVERLAY_SPINNER, state="hidden")
        self.page.wait_for_selector(CartLocators.PROCEED_TO_BUTTON, state="attached")
        proceed_to_checkout_button = self.page.locator(CartLocators.PROCEED_TO_BUTTON)
        expect(proceed_to_checkout_button).to_be_enabled()
        
           
    def click_checkboxes(self):
        """Click all checkboxes one by one in a loop and verify their state"""
        # First unselect all items to start from a clean state
        self.unselect_all_items()
        self.page.wait_for_load_state("networkidle")
        
        # Verify all items are unselected initially
        self.expect_all_items_unselected()
        print("Verified all items are unselected initially")
        
        # Find all checkboxes
        checkboxes = self.page.locator(CartLocators.ITEM_CHECKBOX).all()
        total_checkboxes = len(checkboxes)
        print(f"Found {total_checkboxes} checkboxes to click")
        
        # Click each checkbox one by one
        for i, checkbox in enumerate(checkboxes):
            try:
                # Make sure checkbox is visible
                expect(checkbox).to_be_visible()
                
                # Click the checkbox
                checkbox.click()
                print(f"Clicked checkbox {i+1}/{total_checkboxes}")
                
                # Wait for any network requests to complete
                self.page.wait_for_load_state("networkidle")
                
                # Verify this specific checkbox is now checked
                expect(checkbox).to_be_checked()
                
                # Verify the total number of checked items
                selected_count = self.page.locator(CartLocators.CHECKED_ITEM_CHECKBOX).count()
                print(f"Item {i+1}/{total_checkboxes}: Checked. Total selected: {selected_count}")
                
                # Wait a moment before proceeding to the next checkbox
                self.page.wait_for_timeout(500)
                
            except Exception as e:
                print(f"Error clicking checkbox {i+1}: {str(e)}")
                # Continue with the next checkbox
        
        print(f"Completed clicking {total_checkboxes} checkboxes")
        return total_checkboxes
        