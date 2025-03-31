from .remove_cart_body import REMOVE_CART


class RemoveCartMutation:
    def __init__(self, graphql_client):
        self.graphql_client = graphql_client

    def execute(self, cart_id: str, user_id: str):
        variables = {
            "command": {
                "cartId": cart_id,
                "userId": user_id,
            },
        }

        result = self.graphql_client.execute(REMOVE_CART, variable_values=variables)

        return result
