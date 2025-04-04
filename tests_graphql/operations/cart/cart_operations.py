from gql import Client
from graphql_requests.mutations.add_bulk_items_cart.add_bulk_items_cart_mutation import AddBulkItemsCartMutation
from graphql_requests.mutations.add_item.add_item_mutation import AddItemMutation
from graphql_requests.mutations.add_items_cart.add_items_cart_mutation import AddItemsCartMutation
from graphql_requests.mutations.add_or_update_cart_payment.add_or_update_cart_payment_mutation import (
    AddOrUpdateCartPaymentMutation,
)
from graphql_requests.mutations.add_or_update_cart_shipment.add_or_update_cart_shipment_mutation import (
    AddOrUpdateCartShipmentMutation,
)
from graphql_requests.mutations.clear_cart.clear_cart_mutation import ClearCartMutation
from graphql_requests.mutations.change_cart_item_quantity.change_cart_item_quantity_mutation import (
    ChangeCartItemQuantityMutation,
)
from graphql_requests.mutations.clear_payments.clear_payments_mutation import ClearPaymentsMutation
from graphql_requests.mutations.create_order_from_cart.create_order_from_cart_mutation import (
    CreateOrderFromCartMutation,
)
from graphql_requests.mutations.merge_cart.merge_cart_mutation import MergeCartMutation
from graphql_requests.mutations.remove_cart_address.remove_cart_address_mutation import RemoveCartAddressMutation
from graphql_requests.mutations.remove_cart.remove_cart_mutation import RemoveCartMutation
from graphql_requests.mutations.remove_cart_item.remove_cart_item_mutation import RemoveCartItemMutation
from graphql_requests.mutations.remove_shipment.remove_shipment_mutation import RemoveShipmentMutation
from graphql_requests.mutations.select_all_cart_items.select_all_cart_items_mutation import SelectAllCartItemsMutation
from graphql_requests.mutations.select_cart_items.select_cart_items_mutation import SelectCartItemsMutation
from graphql_requests.mutations.unselect_all_cart_items.unselect_all_cart_items_mutation import (
    UnselectAllCartItemsMutation,
)
from graphql_requests.mutations.unselect_cart_items.unselect_cart_items_mutation import UnselectCartItemsMutation
from graphql_requests.queries.cart.cart_query import CartQuery


class CartOperations:
    def __init__(self, graphql_client: Client):
        self.graphql_client = graphql_client

    def get_cart(self, store_id: str, user_id: str, currency_code: str, culture_name: str):
        """
        Get cart for a user.
        Args:
            store_id (str): ID of the store
            user_id (str): ID of the user whose cart to get
            currency_code (str): Currency code for cart prices (e.g. 'USD')
            culture_name (str): Culture/locale name (e.g. 'en-US')
        Returns:
            dict: Response containing cart data
        """

        cart_query = CartQuery(self.graphql_client)

        result = cart_query.execute(
            store_id=store_id,
            user_id=user_id,
            currency_code=currency_code,
            culture_name=culture_name,
        )

        return result

    def add_item_to_cart(
        self, store_id: str, user_id: str, product_id: str, quantity: int, currency_code: str, culture_name: str
    ):
        """
        Add an item to a user's cart.
        Args:
            store_id (str): ID of the store
            user_id (str): ID of the user whose cart to add to
            product_id (str): ID of the product to add
            quantity (int): Quantity of product to add
            currency_code (str): Currency code for cart prices (e.g. 'USD')
            culture_name (str): Culture/locale name (e.g. 'en-US')
        Returns:
            dict: Response containing updated cart data
        """

        add_item_mutation = AddItemMutation(self.graphql_client)

        result = add_item_mutation.execute(
            store_id=store_id,
            user_id=user_id,
            product_id=product_id,
            quantity=quantity,
            currency_code=currency_code,
            culture_name=culture_name,
        )

        return result

    def change_cart_item_quantity(
        self, store_id: str, user_id: str, currency_code: str, culture_name: str, line_item_id: str, quantity: int
    ):
        """
        Change the quantity of an item in a user's cart.
        Args:
            store_id (str): ID of the store
            user_id (str): ID of the user whose cart to modify
            currency_code (str): Currency code for cart prices (e.g. 'USD')
            culture_name (str): Culture/locale name (e.g. 'en-US')
            line_item_id (str): ID of the line item to modify
            quantity (int): New quantity to set for the item
        Returns:
            dict: Response containing updated cart data
        """

        change_cart_item_quantity_mutation = ChangeCartItemQuantityMutation(self.graphql_client)

        result = change_cart_item_quantity_mutation.execute(
            store_id=store_id,
            user_id=user_id,
            currency_code=currency_code,
            culture_name=culture_name,
            line_item_id=line_item_id,
            quantity=quantity,
        )

        return result

    def select_cart_items(
        self, store_id: str, user_id: str, currency_code: str, culture_name: str, line_item_ids: list[str]
    ):
        """
        Select specific items in a user's cart.
        Args:
            store_id (str): ID of the store
            user_id (str): ID of the user whose cart to modify
            currency_code (str): Currency code for cart prices (e.g. 'USD')
            culture_name (str): Culture/locale name (e.g. 'en-US')
            line_item_ids (list[str]): List of line item IDs to select
        Returns:
            dict: Response containing updated cart data
        """

        select_cart_items_mutation = SelectCartItemsMutation(self.graphql_client)

        result = select_cart_items_mutation.execute(
            store_id=store_id,
            user_id=user_id,
            currency_code=currency_code,
            culture_name=culture_name,
            line_item_ids=line_item_ids,
        )

        return result

    def select_all_cart_items(self, store_id: str, user_id: str, currency_code: str, culture_name: str):
        """
        Select all items in a user's cart.
        Args:
            store_id (str): ID of the store
            user_id (str): ID of the user whose cart to modify
            currency_code (str): Currency code for cart prices (e.g. 'USD')
            culture_name (str): Culture/locale name (e.g. 'en-US')
        Returns:
            dict: Response containing updated cart data
        """

        select_all_cart_items_mutation = SelectAllCartItemsMutation(self.graphql_client)

        result = select_all_cart_items_mutation.execute(
            store_id=store_id,
            user_id=user_id,
            currency_code=currency_code,
            culture_name=culture_name,
        )

        return result

    def unselect_cart_items(
        self, store_id: str, user_id: str, currency_code: str, culture_name: str, line_item_ids: list[str]
    ):
        """
        Unselect specific items in a user's cart.
        Args:
            store_id (str): ID of the store
            user_id (str): ID of the user whose cart to modify
            currency_code (str): Currency code for cart prices (e.g. 'USD')
            culture_name (str): Culture/locale name (e.g. 'en-US')
            line_item_ids (list[str]): List of line item IDs to unselect
        Returns:
            dict: Response containing updated cart data
        """

        unselect_cart_items_mutation = UnselectCartItemsMutation(self.graphql_client)

        result = unselect_cart_items_mutation.execute(
            store_id=store_id,
            user_id=user_id,
            currency_code=currency_code,
            culture_name=culture_name,
            line_item_ids=line_item_ids,
        )

        return result

    def unselect_all_cart_items(self, store_id: str, user_id: str, currency_code: str, culture_name: str):
        """
        Unselect all items in a user's cart.
        Args:
            store_id (str): ID of the store
            user_id (str): ID of the user whose cart to modify
            currency_code (str): Currency code for cart prices (e.g. 'USD')
            culture_name (str): Culture/locale name (e.g. 'en-US')
        Returns:
            dict: Response containing updated cart data
        """

        unselect_all_cart_items_mutation = UnselectAllCartItemsMutation(self.graphql_client)

        result = unselect_all_cart_items_mutation.execute(
            store_id=store_id,
            user_id=user_id,
            currency_code=currency_code,
            culture_name=culture_name,
        )

        return result

    def remove_cart_item(self, store_id: str, user_id: str, currency_code: str, culture_name: str, line_item_id: str):
        """
        Remove an item from a user's cart.
        Args:
            store_id (str): ID of the store
            user_id (str): ID of the user whose cart to modify
            currency_code (str): Currency code for cart prices (e.g. 'USD')
            culture_name (str): Culture/locale name (e.g. 'en-US')
            line_item_id (str): ID of the line item to remove
        Returns:
            dict: Response containing updated cart data
        """

        remove_cart_item_mutation = RemoveCartItemMutation(self.graphql_client)

        result = remove_cart_item_mutation.execute(
            store_id=store_id,
            user_id=user_id,
            currency_code=currency_code,
            culture_name=culture_name,
            line_item_id=line_item_id,
        )

        return result

    def clear_cart(self, store_id: str, user_id: str, currency_code: str, culture_name: str):
        """
        Clear all items from a user's cart.
        Args:
            store_id (str): ID of the store
            user_id (str): ID of the user whose cart to clear
            currency_code (str): Currency code for cart prices (e.g. 'USD')
            culture_name (str): Culture/locale name (e.g. 'en-US')
        Returns:
            dict: Response containing cleared cart data
        """

        clear_cart_mutation = ClearCartMutation(self.graphql_client)

        result = clear_cart_mutation.execute(
            store_id=store_id,
            user_id=user_id,
            currency_code=currency_code,
            culture_name=culture_name,
        )

        return result

    def add_or_update_cart_shipment(self, store_id: str, user_id: str, currency_code: str, culture_name: str, shipment):
        """
        Add or update shipment information for a user's cart.
        Args:
            store_id (str): ID of the store
            user_id (str): ID of the user whose cart to modify
            currency_code (str): Currency code for cart prices (e.g. 'USD')
            culture_name (str): Culture/locale name (e.g. 'en-US')
            shipment: Shipment information to add or update
        Returns:
            dict: Response containing updated cart data
        """

        add_or_update_cart_shipment_mutation = AddOrUpdateCartShipmentMutation(self.graphql_client)

        result = add_or_update_cart_shipment_mutation.execute(
            store_id=store_id,
            user_id=user_id,
            currency_code=currency_code,
            culture_name=culture_name,
            shipment=shipment,
        )

        return result

    def remove_cart_address(self, store_id: str, user_id: str, address_id: str, currency_code: str, culture_name: str):
        """
        Remove an address from a user's cart.
        Args:
            store_id (str): ID of the store
            user_id (str): ID of the user whose cart to modify
            address_id (str): ID of the address to remove
            currency_code (str): Currency code for cart prices (e.g. 'USD')
            culture_name (str): Culture/locale name (e.g. 'en-US')
        Returns:
            dict: Response containing updated cart data
        """

        remove_cart_address_mutation = RemoveCartAddressMutation(self.graphql_client)

        result = remove_cart_address_mutation.execute(
            store_id=store_id,
            user_id=user_id,
            address_id=address_id,
            currency_code=currency_code,
            culture_name=culture_name,
        )

        return result

    def remove_shipment(self, store_id: str, user_id: str, shipment_id: str, currency_code: str, culture_name: str):
        """
        Remove a shipment from a user's cart.
        Args:
            store_id (str): ID of the store
            user_id (str): ID of the user whose cart to modify
            shipment_id (str): ID of the shipment to remove
            currency_code (str): Currency code for cart prices (e.g. 'USD')
            culture_name (str): Culture/locale name (e.g. 'en-US')
        Returns:
            dict: Response containing updated cart data
        """

        create_order_from_cart_mutation = RemoveShipmentMutation(self.graphql_client)

        result = create_order_from_cart_mutation.execute(
            store_id=store_id,
            user_id=user_id,
            shipment_id=shipment_id,
            currency_code=currency_code,
            culture_name=culture_name,
        )

        return result

    def add_or_update_cart_payment(self, store_id: str, user_id: str, currency_code: str, culture_name: str, payment):
        """
        Add or update a payment in a user's cart.
        Args:
            store_id (str): ID of the store
            user_id (str): ID of the user whose cart to modify
            currency_code (str): Currency code for cart prices (e.g. 'USD')
            culture_name (str): Culture/locale name (e.g. 'en-US')
            payment: Payment details to add or update
        Returns:
            dict: Response containing updated cart data
        """

        add_or_update_cart_payment_mutation = AddOrUpdateCartPaymentMutation(self.graphql_client)

        result = add_or_update_cart_payment_mutation.execute(
            store_id=store_id,
            user_id=user_id,
            currency_code=currency_code,
            culture_name=culture_name,
            payment=payment,
        )

        return result

    def clear_payments(self, store_id: str, user_id: str, currency_code: str, culture_name: str):
        """
        Clear all payments from a user's cart.
        Args:
            store_id (str): ID of the store
            user_id (str): ID of the user whose cart to modify
            currency_code (str): Currency code for cart prices (e.g. 'USD')
            culture_name (str): Culture/locale name (e.g. 'en-US')
        Returns:
            dict: Response containing updated cart data
        """

        clear_payments_mutation = ClearPaymentsMutation(self.graphql_client)

        result = clear_payments_mutation.execute(
            store_id=store_id,
            user_id=user_id,
            currency_code=currency_code,
            culture_name=culture_name,
        )

        return result

    def add_items_to_cart(self, store_id: str, user_id: str, currency_code: str, culture_name: str, cart_items: list):
        """
        Add multiple items to a user's cart.
        Args:
            store_id (str): ID of the store
            user_id (str): ID of the user whose cart to modify
            currency_code (str): Currency code for cart prices (e.g. 'USD')
            culture_name (str): Culture/locale name (e.g. 'en-US')
            cart_items (list): List of items to add to the cart
        Returns:
            dict: Response containing updated cart data
        """

        add_items_cart_mutation = AddItemsCartMutation(self.graphql_client)

        result = add_items_cart_mutation.execute(
            store_id=store_id,
            user_id=user_id,
            currency_code=currency_code,
            culture_name=culture_name,
            cart_items=cart_items,
        )

        return result

    def add_bulk_items_to_cart(self, store_id: str, user_id: str, currency_code: str, culture_name: str, cart_items):
        """
        Add multiple items to a user's cart in bulk.
        Args:
            store_id (str): ID of the store
            user_id (str): ID of the user whose cart to modify
            currency_code (str): Currency code for cart prices (e.g. 'USD')
            culture_name (str): Culture/locale name (e.g. 'en-US')
            cart_items (list): List of items to add to the cart in bulk
        Returns:
            dict: Response containing updated cart data
        """

        add_bulk_items_cart_mutation = AddBulkItemsCartMutation(self.graphql_client)

        result = add_bulk_items_cart_mutation.execute(
            store_id=store_id,
            user_id=user_id,
            currency_code=currency_code,
            culture_name=culture_name,
            cart_items=cart_items,
        )

        return result

    def remove_cart(self, cart_id: str, user_id: str):
        """
        Remove a user's cart.
        Args:
            cart_id (str): ID of the cart to remove
            user_id (str): ID of the user whose cart to remove
        Returns:
            dict: Response indicating success of cart removal
        """

        remove_cart_mutation = RemoveCartMutation(self.graphql_client)

        result = remove_cart_mutation.execute(cart_id, user_id)

        return result

    def merge_cart(
        self,
        store_id: str,
        user_id: str,
        currency_code: str,
        culture_name: str,
        second_cart_id: str,
        delete_after_merge: bool = False,
    ):
        """
        Merge two carts together.
        Args:
            store_id (str): ID of the store
            user_id (str): ID of the user whose cart to merge into
            currency_code (str): Currency code for cart prices (e.g. 'USD')
            culture_name (str): Culture/locale name (e.g. 'en-US')
            second_cart_id (str): ID of the cart to merge from
            delete_after_merge (bool): Whether to delete the second cart after merging
        Returns:
            dict: Response containing merged cart data
        """

        merge_cart_mutation = MergeCartMutation(self.graphql_client)

        result = merge_cart_mutation.execute(
            store_id=store_id,
            user_id=user_id,
            currency_code=currency_code,
            culture_name=culture_name,
            second_cart_id=second_cart_id,
            delete_after_merge=delete_after_merge,
        )

        return result

    def create_order_from_cart(self, cart_id: str):
        """
        Create an order from a cart.
        Args:
            cart_id (str): ID of the cart to create order from
        Returns:
            dict: Response containing the created order data
        """

        create_order_from_cart_mutation = CreateOrderFromCartMutation(self.graphql_client)

        result = create_order_from_cart_mutation.execute(cart_id)

        return result
