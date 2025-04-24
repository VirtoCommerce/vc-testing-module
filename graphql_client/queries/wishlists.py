from gql import gql
from graphql_client.types.wishlist_connection import WishlistConnection


class WishlistsQuery:
    def __init__(self, graphql_client):
        self.graphql_client = graphql_client

    def execute(self, variables: dict, return_fields: str = None) -> WishlistConnection:
        query_string = f"""
            query wishlists($after: String, $first: Int, $storeId: String, $userId: String, $currencyCode: String, $cultureName: String, $scope: String, $sort: String) {{
                wishlists(
                    after: $after,
                    first: $first,
                    storeId: $storeId,
                    userId: $userId,
                    currencyCode: $currencyCode,
                    cultureName: $cultureName,
                    scope: $scope,
                    sort: $sort
                ) {{
                    {return_fields}
                }}
            }}
        """

        return self.graphql_client.execute(gql(query_string), variables)["wishlists"]
