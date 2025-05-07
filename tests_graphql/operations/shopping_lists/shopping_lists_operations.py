from gql import Client
from graphql_client.types.wishlist_type import WishlistType
from graphql_client.mutations.create_wishlist import CreateWishlistMutation
from graphql_client.types.input_create_wishlist_type import InputCreateWishlistType
from tests_graphql.operations.shopping_lists.fragments.shopping_list_fragment import SHOPPING_LIST_FRAGMENT
from graphql_client.types.input_remove_wishlist_type import InputRemoveWishlistType
from graphql_client.mutations.remove_wishlist import RemoveWishlistMutation
from graphql_client.types.wishlist_connection import WishlistConnection
from graphql_client.queries.wishlists import WishlistsQuery
from graphql_client.queries.wishlist import WishlistQuery
from graphql_client.mutations.add_wishlist_item import AddWishlistItemMutation
from graphql_client.mutations.change_wishlist import ChangeWishlistMutation
from graphql_client.types.input_change_wishlist_type import InputChangeWishlistType
from graphql_client.types.input_update_wishlist_items_type import InputUpdateWishlistItemsType
from graphql_client.mutations.update_wish_list_items import UpdateWishListItemsMutation
from graphql_client.types.input_remove_wishlist_item_type import InputRemoveWishlistItemType
from graphql_client.mutations.remove_wishlist_item import RemoveWishlistItemMutation


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

    def get_shopping_list(self, list_id: str, culture_name: str) -> WishlistType:
        wishlist_query = WishlistQuery(self.graphql_client)

        variables = {"listId": list_id, "cultureName": culture_name}

        result = wishlist_query.execute(variables=variables, return_fields=SHOPPING_LIST_FRAGMENT)

        return result

    def update_shopping_list(self, list_id: str, payload: InputChangeWishlistType) -> WishlistType:
        change_wishlist_mutation = ChangeWishlistMutation(self.graphql_client)

        variables = {"command": payload}

        result = change_wishlist_mutation.execute(variables=variables, return_fields=SHOPPING_LIST_FRAGMENT)

        return result

    def add_item_to_shopping_list(self, list_id: str, product_id: str, quantity: int) -> WishlistType:
        add_item_to_wishlist_mutation = AddWishlistItemMutation(self.graphql_client)

        variables = {"command": {"listId": list_id, "productId": product_id, "quantity": quantity}}

        result = add_item_to_wishlist_mutation.execute(variables=variables, return_fields=SHOPPING_LIST_FRAGMENT)

        return result

    def update_shopping_list_items(self, payload: InputUpdateWishlistItemsType) -> WishlistType:
        update_wishlist_items_mutation = UpdateWishListItemsMutation(self.graphql_client)

        variables = {"command": payload}

        result = update_wishlist_items_mutation.execute(variables=variables, return_fields=SHOPPING_LIST_FRAGMENT)

        return result

    def remove_shopping_list_item(self, payload: InputRemoveWishlistItemType) -> WishlistType:
        remove_wishlist_item_mutation = RemoveWishlistItemMutation(self.graphql_client)

        variables = {"command": payload}

        result = remove_wishlist_item_mutation.execute(variables=variables, return_fields=SHOPPING_LIST_FRAGMENT)

        return result

    def remove_shopping_list(self, payload: InputRemoveWishlistType) -> None:
        remove_wishlist_mutation = RemoveWishlistMutation(self.graphql_client)

        variables = {"command": payload}

        result = remove_wishlist_mutation.execute(variables=variables, return_fields=None)

        return result
