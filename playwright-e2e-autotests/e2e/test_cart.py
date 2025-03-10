import allure

from e2e.pages.cart import CartPage
from e2e.steps.browser_steps import BrowserSteps
from e2e.steps.graphql_steps import GraphQLSteps


@allure.feature("Cart")
@allure.title("Clear Cart")
@allure.description("This test adds a product to cart and checks if clean cart feature works")
@allure.tag("Cart")
@allure.severity(allure.severity_level.NORMAL)
def test_add_product_to_cart_and_clear_cart(playwright_authenticated_page, graphql_client, user_context, config):
    user_id = user_context["me"]["id"]
    cart_page = CartPage(playwright_authenticated_page, config)
    graphql_steps = GraphQLSteps(graphql_client, user_id)
    browser_steps = BrowserSteps(cart_page)

    graphql_steps.add_product_to_cart("64_2457842", 1, "29650dd4-da96-4d66-8814-4f65da7d686c")

    browser_steps.open_cart()
    browser_steps.check_product_is_in_cart("Logitech HD Webcam C270 - webcam")

    browser_steps.clear_cart()
