from typing import Any

from gql.operations.base_operations import BaseOperations, gql
from gql.types.cart import Cart
from gql.types.cart_item_input import CartItemInput
from gql.types.order import Order
from gql.types.payment_input import PaymentInput
from gql.types.shipment_input import ShipmentInput


class CartOperations(BaseOperations):
    def get_cart(
        self,
        store_id: str,
        user_id: str,
        currency_code: str,
        culture_name: str,
        cart_id: str | None = None,
    ) -> Cart | None:
        # fmt: off
        query = gql("""
            query GetCart($storeId: String!, $userId: String!, $currencyCode: String!, $cultureName: String!, $cartId: String) {
              cart(storeId: $storeId, userId: $userId, currencyCode: $currencyCode, cultureName: $cultureName, cartId: $cartId) {
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
                "cartId": cart_id,
            },
        )
        data = result["data"]["cart"]
        return Cart.model_validate(data) if data else None

    def get_cart_validation(
        self,
        store_id: str,
        user_id: str,
        currency_code: str,
        culture_name: str,
        rule_set: str,
        cart_id: str | None = None,
    ) -> dict[str, Any]:
        """Read cart-level validationErrors for an explicit ruleSet alongside the
        per-line validation fields, returning the raw ``cart`` payload.

        The shared ``CartFragment`` always reads the default ``validationErrors``
        (no ``ruleSet`` argument), so ruleSet-scoped reads need their own query.
        The result is returned as a plain dict because callers assert on the
        per-ruleSet response shape directly.
        """
        # fmt: off
        query = gql("""
            query GetCartValidation($storeId: String!, $userId: String!, $currencyCode: String!, $cultureName: String!, $ruleSet: String, $cartId: String) {
              cart(storeId: $storeId, userId: $userId, currencyCode: $currencyCode, cultureName: $cultureName, cartId: $cartId) {
                itemsCount
                validationErrors(ruleSet: $ruleSet) { errorCode objectType objectId errorMessage }
                items { id sku productId quantity isValid validationErrors { errorCode objectType errorMessage } }
              }
            }
        """)
        # fmt: on
        result = self._client.execute(
            query,
            variables={
                "storeId": store_id,
                "userId": user_id,
                "currencyCode": currency_code,
                "cultureName": culture_name,
                "ruleSet": rule_set,
                "cartId": cart_id,
            },
        )
        return result["data"]["cart"]

    def get_cart_validation_aliased(
        self,
        store_id: str,
        user_id: str,
        currency_code: str,
        culture_name: str,
        rule_set_a: str,
        rule_set_b: str,
        cart_id: str | None = None,
    ) -> dict[str, Any]:
        """Read two ruleSet-scoped cart-level validationErrors within a SINGLE
        request via GraphQL aliases (``errorsA`` / ``errorsB``).

        Used to prove within-request ruleSet cache isolation: resolving one
        ruleSet must not leak its errors into (or poison) the other in the same
        response. Returns the raw ``cart`` payload.
        """
        # fmt: off
        query = gql("""
            query GetCartValidationAliased($storeId: String!, $userId: String!, $currencyCode: String!, $cultureName: String!, $ruleSetA: String, $ruleSetB: String, $cartId: String) {
              cart(storeId: $storeId, userId: $userId, currencyCode: $currencyCode, cultureName: $cultureName, cartId: $cartId) {
                itemsCount
                errorsA: validationErrors(ruleSet: $ruleSetA) { errorCode objectType objectId errorMessage }
                errorsB: validationErrors(ruleSet: $ruleSetB) { errorCode objectType objectId errorMessage }
              }
            }
        """)
        # fmt: on
        result = self._client.execute(
            query,
            variables={
                "storeId": store_id,
                "userId": user_id,
                "currencyCode": currency_code,
                "cultureName": culture_name,
                "ruleSetA": rule_set_a,
                "ruleSetB": rule_set_b,
                "cartId": cart_id,
            },
        )
        return result["data"]["cart"]

    def get_cart_line_validation(
        self,
        store_id: str,
        user_id: str,
        currency_code: str,
        culture_name: str,
        cart_id: str | None = None,
    ) -> dict[str, Any]:
        """Read ONLY the per-line validation fields — no cart-level
        ``validationErrors`` selection.

        This is the decisive VCST-5234 probe: querying cart-level
        ``validationErrors`` re-validates the aggregate and would refill the
        per-line store, masking the bug. Omitting it ensures the per-line
        ``isValid`` / ``validationErrors`` are read straight from the saved
        line. Returns the raw ``cart`` payload.
        """
        # fmt: off
        query = gql("""
            query GetCartLineValidation($storeId: String!, $userId: String!, $currencyCode: String!, $cultureName: String!, $cartId: String) {
              cart(storeId: $storeId, userId: $userId, currencyCode: $currencyCode, cultureName: $cultureName, cartId: $cartId) {
                itemsCount
                items { id sku productId quantity isValid validationErrors { errorCode objectType errorMessage } }
              }
            }
        """)
        # fmt: on
        result = self._client.execute(
            query,
            variables={
                "storeId": store_id,
                "userId": user_id,
                "currencyCode": currency_code,
                "cultureName": culture_name,
                "cartId": cart_id,
            },
        )
        return result["data"]["cart"]

    def add_items_to_cart(
        self,
        store_id: str,
        user_id: str,
        items: list[CartItemInput],
        currency_code: str | None = None,
        culture_name: str | None = None,
    ) -> Cart:
        # fmt: off
        mutation = gql("""
            mutation AddItemsCart($command: InputAddItemsType!) {
              addItemsCart(command: $command) {
                ...CartFragment
              }
            }
        """)
        # fmt: on
        command = {
            "storeId": store_id,
            "userId": user_id,
            "cartItems": [i.model_dump(by_alias=True) for i in items],
            **({"currencyCode": currency_code} if currency_code else {}),
            **({"cultureName": culture_name} if culture_name else {}),
        }
        result = self._client.execute(
            self._build_query(mutation),
            variables={"command": command},
        )
        return Cart.model_validate(result["data"]["addItemsCart"])

    def update_cart_quantity(
        self,
        store_id: str,
        user_id: str,
        items: list[CartItemInput],
        currency_code: str | None = None,
        culture_name: str | None = None,
    ) -> Cart:
        # fmt: off
        mutation = gql("""
            mutation UpdateCartQuantity($command: InputUpdateCartQuantity!) {
              updateCartQuantity(command: $command) {
                ...CartFragment
              }
            }
        """)
        # fmt: on
        command = {
            "storeId": store_id,
            "userId": user_id,
            "items": [i.model_dump(by_alias=True) for i in items],
            **({"currencyCode": currency_code} if currency_code else {}),
            **({"cultureName": culture_name} if culture_name else {}),
        }
        result = self._client.execute(
            self._build_query(mutation),
            variables={"command": command},
        )
        return Cart.model_validate(result["data"]["updateCartQuantity"])

    def add_or_update_cart_payment(
        self,
        store_id: str,
        user_id: str,
        payment: PaymentInput,
        currency_code: str | None = None,
        culture_name: str | None = None,
    ) -> Cart:
        # fmt: off
        mutation = gql("""
            mutation AddOrUpdateCartPayment($command: InputAddOrUpdateCartPaymentType!) {
              addOrUpdateCartPayment(command: $command) {
                ...CartFragment
              }
            }
        """)
        # fmt: on
        command = {
            "storeId": store_id,
            "userId": user_id,
            "payment": payment.model_dump(by_alias=True, exclude_none=True),
            **({"currencyCode": currency_code} if currency_code else {}),
            **({"cultureName": culture_name} if culture_name else {}),
        }
        result = self._client.execute(
            self._build_query(mutation),
            variables={"command": command},
        )
        return Cart.model_validate(result["data"]["addOrUpdateCartPayment"])

    def add_or_update_cart_shipment(
        self,
        store_id: str,
        user_id: str,
        shipment: ShipmentInput,
        cart_id: str | None = None,
        currency_code: str | None = None,
        culture_name: str | None = None,
    ) -> Cart:
        # fmt: off
        mutation = gql("""
            mutation AddOrUpdateCartShipment($command: InputAddOrUpdateCartShipmentType!) {
              addOrUpdateCartShipment(command: $command) {
                ...CartFragment
              }
            }
        """)
        # fmt: on
        command = {
            "storeId": store_id,
            "userId": user_id,
            "shipment": shipment.model_dump(by_alias=True, exclude_none=True),
            **({"cartId": cart_id} if cart_id else {}),
            **({"currencyCode": currency_code} if currency_code else {}),
            **({"cultureName": culture_name} if culture_name else {}),
        }
        result = self._client.execute(
            self._build_query(mutation),
            variables={"command": command},
        )
        return Cart.model_validate(result["data"]["addOrUpdateCartShipment"])

    def add_coupon(
        self,
        store_id: str,
        user_id: str,
        code: str,
        currency_code: str | None = None,
        culture_name: str | None = None,
    ) -> Cart:
        # fmt: off
        mutation = gql("""
            mutation AddCoupon($command: InputAddCouponType!) {
              addCoupon(command: $command) {
                ...CartFragment
              }
            }
        """)
        # fmt: on
        command = {
            "storeId": store_id,
            "userId": user_id,
            "couponCode": code,
            **({"currencyCode": currency_code} if currency_code else {}),
            **({"cultureName": culture_name} if culture_name else {}),
        }
        result = self._client.execute(
            self._build_query(mutation),
            variables={"command": command},
        )
        return Cart.model_validate(result["data"]["addCoupon"])

    def remove_coupon(
        self,
        store_id: str,
        user_id: str,
        code: str,
        currency_code: str | None = None,
        culture_name: str | None = None,
    ) -> Cart:
        # fmt: off
        mutation = gql("""
            mutation RemoveCoupon($command: InputRemoveCouponType!) {
              removeCoupon(command: $command) {
                ...CartFragment
              }
            }
        """)
        # fmt: on
        command = {
            "storeId": store_id,
            "userId": user_id,
            "couponCode": code,
            **({"currencyCode": currency_code} if currency_code else {}),
            **({"cultureName": culture_name} if culture_name else {}),
        }
        result = self._client.execute(
            self._build_query(mutation),
            variables={"command": command},
        )
        return Cart.model_validate(result["data"]["removeCoupon"])

    def clear_cart(
        self,
        cart_id: str,
        store_id: str,
        user_id: str,
        currency_code: str | None = None,
        culture_name: str | None = None,
    ) -> Cart:
        # fmt: off
        mutation = gql("""
            mutation ClearCart($command: InputClearCartType!) {
              clearCart(command: $command) {
                ...CartFragment
              }
            }
        """)
        # fmt: on
        result = self._client.execute(
            self._build_query(mutation),
            variables={
                "command": {
                    "cartId": cart_id,
                    "storeId": store_id,
                    "userId": user_id,
                    **({"currencyCode": currency_code} if currency_code else {}),
                    **({"cultureName": culture_name} if culture_name else {}),
                }
            },
        )
        return Cart.model_validate(result["data"]["clearCart"])

    def merge_cart(
        self,
        store_id: str,
        user_id: str,
        second_cart_id: str,
        currency_code: str | None = None,
        culture_name: str | None = None,
    ) -> Cart:
        # fmt: off
        mutation = gql("""
            mutation MergeCart($command: InputMergeCartType!) {
              mergeCart(command: $command) {
                ...CartFragment
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
                    "secondCartId": second_cart_id,
                    **({"currencyCode": currency_code} if currency_code else {}),
                    **({"cultureName": culture_name} if culture_name else {}),
                }
            },
        )
        return Cart.model_validate(result["data"]["mergeCart"])

    def select_cart_items(
        self,
        store_id: str,
        user_id: str,
        line_item_ids: list[str],
        cart_id: str | None = None,
        currency_code: str | None = None,
        culture_name: str | None = None,
    ) -> Cart:
        # fmt: off
        mutation = gql("""
            mutation SelectCartItems($command: InputChangeCartItemsSelectedType!) {
              selectCartItems(command: $command) {
                ...CartFragment
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
                    "lineItemIds": line_item_ids,
                    **({"cartId": cart_id} if cart_id else {}),
                    **({"currencyCode": currency_code} if currency_code else {}),
                    **({"cultureName": culture_name} if culture_name else {}),
                }
            },
        )
        return Cart.model_validate(result["data"]["selectCartItems"])

    def unselect_cart_items(
        self,
        store_id: str,
        user_id: str,
        line_item_ids: list[str],
        cart_id: str | None = None,
        currency_code: str | None = None,
        culture_name: str | None = None,
    ) -> Cart:
        # fmt: off
        mutation = gql("""
            mutation UnSelectCartItems($command: InputChangeCartItemsSelectedType!) {
              unSelectCartItems(command: $command) {
                ...CartFragment
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
                    "lineItemIds": line_item_ids,
                    **({"cartId": cart_id} if cart_id else {}),
                    **({"currencyCode": currency_code} if currency_code else {}),
                    **({"cultureName": culture_name} if culture_name else {}),
                }
            },
        )
        return Cart.model_validate(result["data"]["unSelectCartItems"])

    def unselect_all_cart_items(
        self,
        store_id: str,
        user_id: str,
        cart_id: str | None = None,
        currency_code: str | None = None,
        culture_name: str | None = None,
    ) -> Cart:
        # fmt: off
        mutation = gql("""
            mutation UnSelectAllCartItems($command: InputChangeAllCartItemsSelectedType!) {
              unSelectAllCartItems(command: $command) {
                ...CartFragment
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
                    **({"cartId": cart_id} if cart_id else {}),
                    **({"currencyCode": currency_code} if currency_code else {}),
                    **({"cultureName": culture_name} if culture_name else {}),
                }
            },
        )
        return Cart.model_validate(result["data"]["unSelectAllCartItems"])

    def remove_cart_item(
        self,
        store_id: str,
        user_id: str,
        line_item_id: str,
        cart_id: str | None = None,
        currency_code: str | None = None,
        culture_name: str | None = None,
    ) -> Cart:
        # fmt: off
        mutation = gql("""
            mutation RemoveCartItem($command: InputRemoveItemType!) {
              removeCartItem(command: $command) {
                ...CartFragment
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
                    "lineItemId": line_item_id,
                    **({"cartId": cart_id} if cart_id else {}),
                    **({"currencyCode": currency_code} if currency_code else {}),
                    **({"cultureName": culture_name} if culture_name else {}),
                }
            },
        )
        return Cart.model_validate(result["data"]["removeCartItem"])

    def delete_cart(self, cart_id: str, user_id: str) -> bool:
        # fmt: off
        mutation = gql("""
            mutation RemoveCart($command: InputRemoveCartType!) {
              removeCart(command: $command)
            }
        """)
        # fmt: on
        result = self._client.execute(
            self._build_query(mutation),
            variables={"command": {"cartId": cart_id, "userId": user_id}},
        )
        return result["data"]["removeCart"]

    def create_order_from_cart(self, cart_id: str) -> Order:
        # fmt: off
        mutation = gql("""
            mutation CreateOrderFromCart($command: InputCreateOrderFromCartType!) {
              createOrderFromCart(command: $command) {
                ...OrderFragment
              }
            }
        """)
        # fmt: on
        result = self._client.execute(
            self._build_query(mutation),
            variables={"command": {"cartId": cart_id}},
        )
        return Order.model_validate(result["data"]["createOrderFromCart"])
