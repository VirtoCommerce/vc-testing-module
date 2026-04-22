from gql import Client

from graphql_client.mutations.move_from_saved_for_later import (
    MoveFromSavedForLaterMutation,
)
from graphql_client.mutations.move_to_saved_for_later import MoveToSavedForLaterMutation
from graphql_client.mutations.remove_wishlist_item import RemoveWishlistItemMutation
from graphql_client.queries.get_saved_for_later import GetSavedForLaterQuery
from graphql_client.types.cart_type import CartType
from graphql_client.types.cart_with_list_type import CartWithListType
from graphql_client.types.input_remove_wishlist_item_type import (
    InputRemoveWishlistItemType,
)
from graphql_client.types.input_save_for_later_type import InputSaveForLaterType
from graphql_client.types.wishlist_type import WishlistType
from graphql_operations.cart.fragments.cart_fragment import CART_FRAGMENT


class SavedForLaterOperations:
    def __init__(self, graphql_client: Client):
        self.graphql_client = graphql_client

    def move_to_saved_for_later(self, payload: InputSaveForLaterType) -> CartWithListType:
        move_to_saved_for_later_mutation = MoveToSavedForLaterMutation(self.graphql_client)

        variables = {"command": payload}

        return_fields = f"""
            cart {{
                {CART_FRAGMENT}
            }}
            list {{
                {CART_FRAGMENT}
            }}
        """

        result = move_to_saved_for_later_mutation.execute(variables=variables, return_fields=return_fields)

        return result

    def move_from_saved_for_later(self, payload: InputSaveForLaterType) -> CartWithListType:
        move_from_saved_for_later_mutation = MoveFromSavedForLaterMutation(self.graphql_client)

        variables = {"command": payload}

        return_fields = f"""
            cart {{
                {CART_FRAGMENT}
            }}
            list {{
                {CART_FRAGMENT}
            }}
        """

        result = move_from_saved_for_later_mutation.execute(variables=variables, return_fields=return_fields)

        return result

    def get_saved_for_later(
        self,
        store_id: str,
        user_id: str,
        currency_code: str,
        culture_name: str,
        organization_id: str | None = None,
    ) -> CartType:
        get_saved_for_later_query = GetSavedForLaterQuery(self.graphql_client)

        variables = {
            "storeId": store_id,
            "userId": user_id,
            "currencyCode": currency_code,
            "cultureName": culture_name,
        }

        if organization_id:
            variables["organizationId"] = organization_id

        result = get_saved_for_later_query.execute(variables=variables, return_fields=CART_FRAGMENT)

        return result

    def remove_saved_for_later_item(self, payload: InputRemoveWishlistItemType) -> WishlistType:
        """Remove item from saved for later list."""
        remove_wishlist_item_mutation = RemoveWishlistItemMutation(self.graphql_client)

        variables = {"command": payload}

        return_fields = """
            id
            items {
                id
                productId
            }
        """

        result = remove_wishlist_item_mutation.execute(variables=variables, return_fields=return_fields)

        return result
