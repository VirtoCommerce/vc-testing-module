from gql.types.cart import Cart
from gql.types.cart_with_list import CartWithList

from .base_operations import BaseOperations, gql


class SaveForLaterOperations(BaseOperations):
    def get_saved_for_later(
        self,
        store_id: str,
        user_id: str,
        currency_code: str | None = None,
        culture_name: str | None = None,
    ) -> Cart | None:
        # fmt: off
        query = gql("""
            query GetSavedForLater(
                $storeId: String!,
                $userId: String!,
                $currencyCode: String,
                $cultureName: String,
            ) {
              getSavedForLater(
                storeId: $storeId,
                userId: $userId,
                currencyCode: $currencyCode,
                cultureName: $cultureName,
              ) {
                ...CartFragment
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
        data = result["data"]["getSavedForLater"]
        return Cart.model_validate(data) if data else None

    def move_to_saved_for_later(
        self,
        store_id: str,
        user_id: str,
        cart_id: str,
        line_item_ids: list[str],
        currency_code: str | None = None,
        culture_name: str | None = None,
    ) -> CartWithList:
        # fmt: off
        mutation = gql("""
            mutation MoveToSavedForLater($command: InputSaveForLaterType!) {
              moveToSavedForLater(command: $command) {
                ...CartWithListFragment
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
                    "cartId": cart_id,
                    "lineItemIds": line_item_ids,
                    **({"currencyCode": currency_code} if currency_code else {}),
                    **({"cultureName": culture_name} if culture_name else {}),
                }
            },
        )
        return CartWithList.model_validate(result["data"]["moveToSavedForLater"])

    def move_from_saved_for_later(
        self,
        store_id: str,
        user_id: str,
        cart_id: str,
        line_item_ids: list[str],
        currency_code: str | None = None,
        culture_name: str | None = None,
    ) -> CartWithList:
        # fmt: off
        mutation = gql("""
            mutation MoveFromSavedForLater($command: InputSaveForLaterType!) {
              moveFromSavedForLater(command: $command) {
                ...CartWithListFragment
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
                    "cartId": cart_id,
                    "lineItemIds": line_item_ids,
                    **({"currencyCode": currency_code} if currency_code else {}),
                    **({"cultureName": culture_name} if culture_name else {}),
                }
            },
        )
        return CartWithList.model_validate(result["data"]["moveFromSavedForLater"])
