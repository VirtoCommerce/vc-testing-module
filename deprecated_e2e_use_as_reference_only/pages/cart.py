from e2e.pages import BasePage


class CartPage(BasePage):

    def __init__(self, page, config):
        super().__init__(page, config)
        self.url = f'{config["base_url"]}/cart'
        self.button_clear_cart = page.get_by_role("button", name="Clear cart")
        self.button_popup_delete = self.page.get_by_role("button", name="Delete")
        self.product_list = self.page.locator("#products")
        self.cart_is_empty_heading = page.get_by_role("heading", name="Your cart is empty")

    def open(self):
        self.page.goto(self.url)
