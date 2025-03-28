import allure
from gql import Client
from graphql_requests.mutations.add_item.add_item_mutation import AddItemMutation
from graphql_requests.mutations.clear_cart.clear_cart_mutation import ClearCartMutation
from graphql_requests.mutations.create_order_from_cart.create_order_from_cart_mutation import (
    CreateOrderFromCartMutation,
)
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

    def create_order_from_cart(self, cart_id: str):
        """
        Create an order from the specified cart.
        Args:
            cart_id (str): ID of the cart to create order from
        Returns:
            dict: Response containing the created order data
        """

        create_order_from_cart_mutation = CreateOrderFromCartMutation(self.graphql_client)

        result = create_order_from_cart_mutation.execute(cart_id)

        return result
