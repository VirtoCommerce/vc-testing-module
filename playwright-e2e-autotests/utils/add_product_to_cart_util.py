from tests_visual.test_data.test_product import TEST_PRODUCT
from graphql_requests.add_products_to_cart.add_products_to_cart_body import (
    ADD_PRODUCTS_TO_CART,
)
from graphql_requests.get_full_cart.get_full_cart_request import GetFullCartRequest


def add_test_product_to_cart(graphql_client, user_context, product_data=TEST_PRODUCT):
    """
    Add test product to cart using GraphQL request and verify it's added

    Args:
        graphql_client: GraphQL client instance
        user_context: User context containing user ID
        product_data: Dictionary containing productId, quantity, supplierId and name
    """
    variables = {
        "command": {
            "storeId": "",
            "cultureName": "en-US",
            "currencyCode": "USD",
            "userId": user_context["me"]["id"],
            "productId": product_data["productId"],
            "quantity": product_data["quantity"],
        }
    }
    graphql_client.execute(ADD_PRODUCTS_TO_CART, variable_values=variables)

    # Verify product is in cart using GraphQL
    get_cart = GetFullCartRequest(graphql_client)
    cart = get_cart.execute(user_context["me"]["id"])

    # Verify the product name is in the cart items
    cart_items = cart["cart"]["items"]
    assert any(
        item["name"] == product_data["name"] for item in cart_items
    ), f"Product '{product_data['name']}' not found in cart"
