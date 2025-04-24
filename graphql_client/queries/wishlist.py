from gql import gql
from graphql_client.types.wishlist_type import WishlistType


class WishlistQuery:
    def __init__(self, graphql_client):
        self.graphql_client = graphql_client

    def execute(self, variables: dict, return_fields: str = None) -> WishlistType:
        query_string = f"""
            query wishlist($listId: String!, $cultureName: String) {{
                wishlist(
                    listId: $listId,
                    cultureName: $cultureName
                ) {{
                    {return_fields}
                }}
            }}
        """

        return self.graphql_client.execute(gql(query_string), variables)["wishlist"]
