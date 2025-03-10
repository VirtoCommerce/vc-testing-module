import allure
from .clear_cart_body import CLEAR_CART


class ClearCartRequest:
    def __init__(self, graphql_client):
        self.client = graphql_client

    @allure.step("Clear cart (GraphQL)")
    def execute(
        self,
        user_id,
        cart_id,
        store_id="",
        currency_code="USD",
        culture_name="en-US",
    ):
        variables = {
            "command": {
                "storeId": store_id,
                "cultureName": culture_name,
                "currencyCode": currency_code,
                "userId": user_id,
                "cartId": cart_id,
            },
            "skipQuery": False,
        }
        result = self.client.execute(CLEAR_CART, variable_values=variables)
        return result
