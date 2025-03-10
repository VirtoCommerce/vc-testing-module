import allure
from gql import gql
from graphql_requests.get_full_cart.get_full_cart_body import GET_FULL_CART


class GetFullCartRequest:
    def __init__(self, client):
        self.client = client

    @allure.step("Get full cart (GraphQL)")
    def execute(self, user_id):
        """
        Execute GetFullCart request
        Args:
            user_id: User ID
        Returns:
            Cart data
        """
        variables = {
            "storeId": "",
            "cultureName": "en-US",
            "currencyCode": "USD",
            "userId": user_id,
        }
        result = self.client.execute(GET_FULL_CART, variable_values=variables)
        return result
