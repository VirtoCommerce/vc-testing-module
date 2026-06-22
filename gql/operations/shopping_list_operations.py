from gql.operations.base_operations import BaseOperations, gql
from gql.types.cart_item_input import CartItemInput
from gql.types.shopping_list import ShoppingList


class ShoppingListOperations(BaseOperations):
    def get_shopping_list(
        self, list_id: str, culture_name: str | None = None
    ) -> ShoppingList:
        # fmt: off
        query = gql("""
            query GetShoppingList($listId: String!, $cultureName: String) {
              wishlist(listId: $listId, cultureName: $cultureName) {
                ...ShoppingListFragment
              }
            }
        """)
        # fmt: on
        result = self._client.execute(
            self._build_query(query),
            variables={"listId": list_id, "cultureName": culture_name},
        )
        return ShoppingList.model_validate(result["data"]["wishlist"])

    def get_shopping_lists(
        self,
        store_id: str,
        user_id: str,
        currency_code: str | None = None,
        culture_name: str | None = None,
    ) -> list[ShoppingList]:
        # fmt: off
        query = gql("""
            query GetShoppingLists(
              $storeId: String
              $userId: String
              $currencyCode: String
              $cultureName: String
            ) {
              wishlists(
                storeId: $storeId
                userId: $userId
                currencyCode: $currencyCode
                cultureName: $cultureName
              ) {
                items {
                  ...ShoppingListFragment
                }
              }
            }
        """)
        # fmt: on
        result = self._client.execute(
            self._build_query(query),
            variables={
                "storeId": store_id,
                "userId": user_id,
                "currencyCode": currency_code,
                "cultureName": culture_name,
            },
        )
        items = result["data"]["wishlists"]["items"] or []
        return [ShoppingList.model_validate(i) for i in items]

    def create_shopping_list(
        self,
        store_id: str,
        user_id: str,
        name: str | None = None,
        currency_code: str | None = None,
        culture_name: str | None = None,
        description: str | None = None,
    ) -> ShoppingList:
        # fmt: off
        mutation = gql("""
            mutation CreateShoppingList($command: InputCreateWishlistType!) {
              createWishlist(command: $command) {
                ...ShoppingListFragment
              }
            }
        """)
        # fmt: on
        result = self._client.execute(
            self._build_query(mutation),
            variables={
                "command": {
                    "storeId": store_id,
                    "userId": user_id,
                    **({"listName": name} if name else {}),
                    **({"currencyCode": currency_code} if currency_code else {}),
                    **({"cultureName": culture_name} if culture_name else {}),
                    **({"description": description} if description else {}),
                }
            },
        )
        return ShoppingList.model_validate(result["data"]["createWishlist"])

    def change_shopping_list(
        self,
        list_id: str,
        name: str | None = None,
        description: str | None = None,
        scope: str | None = None,
    ) -> ShoppingList:
        # fmt: off
        mutation = gql("""
            mutation ChangeShoppingList($command: InputChangeWishlistType!) {
              changeWishlist(command: $command) {
                ...ShoppingListFragment
              }
            }
        """)
        # fmt: on
        result = self._client.execute(
            self._build_query(mutation),
            variables={
                "command": {
                    "listId": list_id,
                    **({"listName": name} if name is not None else {}),
                    **({"description": description} if description is not None else {}),
                    **({"scope": scope} if scope is not None else {}),
                }
            },
        )
        return ShoppingList.model_validate(result["data"]["changeWishlist"])

    def delete_shopping_list(self, list_id: str) -> bool:
        # fmt: off
        mutation = gql("""
            mutation DeleteShoppingList($command: InputRemoveWishlistType!) {
              removeWishlist(command: $command)
            }
        """)
        # fmt: on
        result = self._client.execute(
            self._build_query(mutation),
            variables={"command": {"listId": list_id}},
        )
        return result["data"]["removeWishlist"]

    def add_items_to_shopping_list(
        self, list_id: str, items: list[CartItemInput]
    ) -> ShoppingList:
        # fmt: off
        mutation = gql("""
            mutation AddItemsToShoppingList($command: InputAddWishlistItemsType!) {
              addWishlistItems(command: $command) {
                ...ShoppingListFragment
              }
            }
        """)
        # fmt: on
        result = self._client.execute(
            self._build_query(mutation),
            variables={
                "command": {
                    "listId": list_id,
                    "listItems": [i.model_dump(by_alias=True) for i in items],
                }
            },
        )
        return ShoppingList.model_validate(result["data"]["addWishlistItems"])

    def update_shopping_list_items(
        self, list_id: str, items: list[tuple[str, int]]
    ) -> ShoppingList:
        # fmt: off
        mutation = gql("""
            mutation UpdateShoppingListItems($command: InputUpdateWishlistItemsType!) {
              updateWishListItems(command: $command) {
                ...ShoppingListFragment
              }
            }
        """)
        # fmt: on
        result = self._client.execute(
            self._build_query(mutation),
            variables={
                "command": {
                    "listId": list_id,
                    "items": [
                        {"lineItemId": line_item_id, "quantity": quantity}
                        for line_item_id, quantity in items
                    ],
                }
            },
        )
        return ShoppingList.model_validate(result["data"]["updateWishListItems"])

    def add_bulk_item_to_shopping_list(
        self, list_id: str, product_id: str, quantity: int = 1
    ) -> ShoppingList:
        # fmt: off
        mutation = gql("""
            mutation AddBulkItemToShoppingList($command: InputAddWishlistBulkItemType!) {
              addWishlistBulkItem(command: $command) {
                wishlists {
                  ...ShoppingListFragment
                }
              }
            }
        """)
        # fmt: on
        result = self._client.execute(
            self._build_query(mutation),
            variables={
                "command": {
                    "listIds": [list_id],
                    "productId": product_id,
                    "quantity": quantity,
                }
            },
        )
        return ShoppingList.model_validate(
            result["data"]["addWishlistBulkItem"]["wishlists"][0]
        )

    def remove_items_from_shopping_list(
        self, list_id: str, line_item_ids: list[str]
    ) -> ShoppingList:
        # fmt: off
        mutation = gql("""
            mutation RemoveItemsFromShoppingList($command: InputRemoveWishlistItemsType!) {
              removeWishlistItems(command: $command) {
                ...ShoppingListFragment
              }
            }
        """)
        # fmt: on
        result = self._client.execute(
            self._build_query(mutation),
            variables={
                "command": {
                    "listId": list_id,
                    "lineItemIds": line_item_ids,
                }
            },
        )
        return ShoppingList.model_validate(result["data"]["removeWishlistItems"])
