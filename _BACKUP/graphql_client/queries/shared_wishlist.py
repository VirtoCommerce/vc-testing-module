from gql import gql
from graphql_client.types.wishlist_type import WishlistType


class SharedWishlistQuery:
    def __init__(self, graphql_client):
        self.graphql_client = graphql_client

    def execute(self, variables: dict, return_fields: str = None) -> WishlistType:
        query_string = f"""
            query sharedWishlist($sharingKey: String!) {{
                sharedWishlist(
                    sharingKey: $sharingKey
                ) {{
                    {return_fields}
                }}
            }}
        """

        return self.graphql_client.execute(gql(query_string), variables)["sharedWishlist"]
