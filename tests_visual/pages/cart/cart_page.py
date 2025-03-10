from .cart_locators import CartLocators


class CartPage:
    def __init__(self, page, config, graphql_client=None, user_context=None):
        self.page = page
        self.config = config
        self.graphql_client = graphql_client
        self.user_context = user_context
        self.locators = CartLocators()

    def navigate(self):
        """Navigate to cart page"""
        self.page.goto(f"{self.config['base_url']}/cart")
        self.page.wait_for_load_state("networkidle")
        self.page.wait_for_load_state("domcontentloaded")

    def proceed_to_shipping(self):
        """Click proceed to checkout button"""
        self.page.get_by_role("link", name=self.locators.PROCEED_CHECKOUT_BUTTON).click()
        self.page.wait_for_url(f"{self.config['base_url']}/checkout/shipping")
        self.page.wait_for_load_state("networkidle")
        self.page.wait_for_load_state("domcontentloaded")
