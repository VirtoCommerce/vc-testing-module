import allure
from .add_products_to_cart_body import ADD_PRODUCTS_TO_CART


class AddProductsToCartRequest:
    def __init__(self, graphql_client):
        self.client = graphql_client

    @allure.step("Add product to cart (GraphQL)")
    def execute(self, user_id, product_id, quantity, item_id):
        variables = {
            "command": {
                "storeId": "",
                "cultureName": "en-US",
                "currencyCode": "USD",
                "userId": user_id,
                "productId": product_id,
                "quantity": quantity,
            }
        }
        result = self.client.execute(ADD_PRODUCTS_TO_CART, variable_values=variables)
        return result
