from gql import gql
from graphql_client.types.cart_type import CartType


class CartQuery:
    def __init__(self, graphql_client):
        self.graphql_client = graphql_client

    def execute(self, variables: dict, return_fields: str = None) -> CartType:
        query_string = f"""
            query cart($cartId: String, $storeId: String!, $currencyCode: String!, $cartType: String, $cartName: String, $userId: String, $cultureName: String) {{
                cart(
                    cartId: $cartId,
                    storeId: $storeId,
                    currencyCode: $currencyCode,
                    cartType: $cartType,
                    cartName: $cartName,
                    userId: $userId,
                    cultureName: $cultureName
                ) {{
                    {return_fields}
                }}
            }}
        """

        return self.graphql_client.execute(gql(query_string), variables)["cart"]
