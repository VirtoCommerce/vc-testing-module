from gql import Client
from graphql_client.types.wishlist_type import WishlistType
from graphql_client.mutations.create_wishlist import CreateWishlistMutation
from graphql_client.types.input_create_wishlist_type import InputCreateWishlistType
from tests_graphql.operations.shopping_lists.fragments.shopping_list_fragment import SHOPPING_LIST_FRAGMENT
from graphql_client.types.input_remove_wishlist_type import InputRemoveWishlistType
from graphql_client.mutations.remove_wishlist import RemoveWishlistMutation
from graphql_client.types.wishlist_connection import WishlistConnection
from graphql_client.queries.wishlists import WishlistsQuery


class ShoppingListsOperations:
    def __init__(self, graphql_client: Client):
        self.graphql_client = graphql_client

    def create_shopping_list(self, payload: InputCreateWishlistType) -> WishlistType:
        create_wishlist_mutation = CreateWishlistMutation(self.graphql_client)

        variables = {"command": payload}

        result = create_wishlist_mutation.execute(variables=variables, return_fields=SHOPPING_LIST_FRAGMENT)

        return result

    def get_shopping_lists(
        self, store_id: str, user_id: str, currency_code: str, culture_name: str
    ) -> WishlistConnection:
        wishlists_query = WishlistsQuery(self.graphql_client)

        variables = {"storeId": store_id, "userId": user_id, "currencyCode": currency_code, "cultureName": culture_name}

        return_fields = """
            totalCount
        """

        result = wishlists_query.execute(variables=variables, return_fields=return_fields)

        return result

    def remove_shopping_list(self, payload: InputRemoveWishlistType) -> None:
        remove_wishlist_mutation = RemoveWishlistMutation(self.graphql_client)

        variables = {"command": payload}

        result = remove_wishlist_mutation.execute(variables=variables, return_fields=None)

        return result
