from gql import gql
from graphql_client.types.cart_connection import CartConnection


class CartsQuery:
    def __init__(self, graphql_client):
        self.graphql_client = graphql_client

    def execute(self, variables: dict, return_fields: str = None) -> CartConnection:
        query_string = f"""
            query carts($after: String, $first: Int, $sort: String, $storeId: String, $userId: String, $currencyCode: String, $cultureName: String, $cartType: String, $filter: String) {{
                carts(
                    after: $after,
                    first: $first,
                    sort: $sort,
                    storeId: $storeId,
                    userId: $userId,
                    currencyCode: $currencyCode,
                    cultureName: $cultureName,
                    cartType: $cartType,
                    filter: $filter
                ) {{
                    {return_fields}
                }}
            }}
        """

        return self.graphql_client.execute(gql(query_string), variables)["carts"]
