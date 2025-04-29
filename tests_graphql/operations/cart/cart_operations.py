from gql import Client
from graphql_client.queries.cart import CartQuery
from graphql_client.types.cart_type import CartType
from graphql_client.mutations.add_item import AddItemMutation
from graphql_client.types.input_add_item_type import InputAddItemType
from graphql_client.mutations.remove_cart import RemoveCartMutation
from graphql_client.types.input_remove_cart_type import InputRemoveCartType
from tests_graphql.operations.cart.cart_fragment import CART_FRAGMENT
from tests_graphql.operations.order.order_fragment import ORDER_FRAGMENT
from graphql_client.types.input_add_items_type import InputAddItemsType
from graphql_client.mutations.add_items_cart import AddItemsCartMutation
from graphql_client.types.input_add_bulk_items_type import InputAddBulkItemsType
from graphql_client.mutations.add_bulk_items_cart import AddBulkItemsCartMutation
from graphql_client.types.bulk_cart_type import BulkCartType
from graphql_client.types.input_add_or_update_cart_payment_type import InputAddOrUpdateCartPaymentType
from graphql_client.mutations.add_or_update_cart_payment import AddOrUpdateCartPaymentMutation
from graphql_client.types.input_remove_cart_address_type import InputRemoveCartAddressType
from graphql_client.mutations.remove_cart_address import RemoveCartAddressMutation
from graphql_client.types.input_clear_payments_type import InputClearPaymentsType
from graphql_client.mutations.clear_payments import ClearPaymentsMutation
from graphql_client.types.input_add_or_update_cart_shipment_type import InputAddOrUpdateCartShipmentType
from graphql_client.mutations.add_or_update_cart_shipment import AddOrUpdateCartShipmentMutation
from graphql_client.types.input_clear_shipments_type import InputClearShipmentsType
from graphql_client.mutations.clear_shipments import ClearShipmentsMutation
from graphql_client.types.input_change_cart_item_quantity_type import InputChangeCartItemQuantityType
from graphql_client.mutations.change_cart_item_quantity import ChangeCartItemQuantityMutation
from graphql_client.types.input_clear_cart_type import InputClearCartType
from graphql_client.mutations.clear_cart import ClearCartMutation
from graphql_client.types.input_create_order_from_cart_type import InputCreateOrderFromCartType
from graphql_client.mutations.create_order_from_cart import CreateOrderFromCartMutation
from graphql_client.types.customer_order_type import CustomerOrderType
from graphql_client.types.input_merge_cart_type import InputMergeCartType
from graphql_client.mutations.merge_cart import MergeCartMutation
from graphql_client.types.input_remove_item_type import InputRemoveItemType
from graphql_client.mutations.remove_cart_item import RemoveCartItemMutation
from graphql_client.types.input_change_cart_items_selected_type import InputChangeCartItemsSelectedType
from graphql_client.mutations.select_cart_items import SelectCartItemsMutation
from graphql_client.types.input_change_all_cart_items_selected_type import InputChangeAllCartItemsSelectedType
from graphql_client.mutations.select_all_cart_items import SelectAllCartItemsMutation
from graphql_client.mutations.un_select_cart_items import UnSelectCartItemsMutation
from graphql_client.mutations.un_select_all_cart_items import UnSelectAllCartItemsMutation
from graphql_client.mutations.add_coupon import AddCouponMutation
from graphql_client.types.input_add_coupon_type import InputAddCouponType
from graphql_client.mutations.remove_coupon import RemoveCouponMutation
from graphql_client.types.input_remove_coupon_type import InputRemoveCouponType


class CartOperations:
    def __init__(self, graphql_client: Client):
        self.graphql_client = graphql_client

    def get_cart(self, store_id: str, user_id: str, currency_code: str, culture_name: str) -> CartType:
        cart_query = CartQuery(self.graphql_client)

        variables = {"storeId": store_id, "userId": user_id, "currencyCode": currency_code, "cultureName": culture_name}

        result = cart_query.execute(variables=variables, return_fields=CART_FRAGMENT)

        return result

    def add_item_to_cart(self, payload: InputAddItemType) -> CartType:
        add_item_mutation = AddItemMutation(self.graphql_client)

        variables = {"command": payload}

        result = add_item_mutation.execute(variables=variables, return_fields=CART_FRAGMENT)

        return result

    def add_items_to_cart(self, payload: InputAddItemsType) -> CartType:
        add_items_mutation = AddItemsCartMutation(self.graphql_client)

        variables = {"command": payload}

        result = add_items_mutation.execute(variables=variables, return_fields=CART_FRAGMENT)

        return result

    def add_bulk_items_to_cart(self, payload: InputAddBulkItemsType) -> BulkCartType:
        add_bulk_items_mutation = AddBulkItemsCartMutation(self.graphql_client)

        variables = {"command": payload}

        return_fields = f"""
            cart {{
                {CART_FRAGMENT}
            }}
            errors {{
                errorCode
                objectId
            }}
        """

        result = add_bulk_items_mutation.execute(variables=variables, return_fields=return_fields)

        return result

    def change_cart_item_quantity(self, payload: InputChangeCartItemQuantityType) -> CartType:
        change_cart_item_quantity_mutation = ChangeCartItemQuantityMutation(self.graphql_client)

        variables = {"command": payload}

        result = change_cart_item_quantity_mutation.execute(variables=variables, return_fields=CART_FRAGMENT)

        return result

    def merge_cart(self, payload: InputMergeCartType) -> CartType:
        merge_cart_mutation = MergeCartMutation(self.graphql_client)

        variables = {"command": payload}

        result = merge_cart_mutation.execute(variables=variables, return_fields=CART_FRAGMENT)

        return result

    def select_cart_items(self, payload: InputChangeCartItemsSelectedType) -> CartType:
        select_cart_items_mutation = SelectCartItemsMutation(self.graphql_client)

        variables = {"command": payload}

        result = select_cart_items_mutation.execute(variables=variables, return_fields=CART_FRAGMENT)

        return result

    def select_all_cart_items(self, payload: InputChangeAllCartItemsSelectedType) -> CartType:
        select_all_cart_items_mutation = SelectAllCartItemsMutation(self.graphql_client)

        variables = {"command": payload}

        result = select_all_cart_items_mutation.execute(variables=variables, return_fields=CART_FRAGMENT)

        return result

    def unselect_cart_items(self, payload: InputChangeCartItemsSelectedType) -> CartType:
        unselect_cart_items_mutation = UnSelectCartItemsMutation(self.graphql_client)

        variables = {"command": payload}

        result = unselect_cart_items_mutation.execute(variables=variables, return_fields=CART_FRAGMENT)

        return result

    def unselect_all_cart_items(self, payload: InputChangeAllCartItemsSelectedType) -> CartType:
        unselect_all_cart_items_mutation = UnSelectAllCartItemsMutation(self.graphql_client)

        variables = {"command": payload}

        result = unselect_all_cart_items_mutation.execute(variables=variables, return_fields=CART_FRAGMENT)

        return result

    def remove_cart_item(self, payload: InputRemoveItemType) -> CartType:
        remove_cart_item_mutation = RemoveCartItemMutation(self.graphql_client)

        variables = {"command": payload}

        result = remove_cart_item_mutation.execute(variables=variables, return_fields=CART_FRAGMENT)

        return result

    def add_or_update_cart_payment(self, payload: InputAddOrUpdateCartPaymentType) -> CartType:
        add_or_update_cart_payment_mutation = AddOrUpdateCartPaymentMutation(self.graphql_client)

        variables = {"command": payload}

        result = add_or_update_cart_payment_mutation.execute(variables=variables, return_fields=CART_FRAGMENT)

        return result

    def add_or_update_cart_shipment(self, payload: InputAddOrUpdateCartShipmentType) -> CartType:
        add_or_update_cart_shipment_mutation = AddOrUpdateCartShipmentMutation(self.graphql_client)

        variables = {"command": payload}

        result = add_or_update_cart_shipment_mutation.execute(variables=variables, return_fields=CART_FRAGMENT)

        return result

    def create_order_from_cart(self, payload: InputCreateOrderFromCartType) -> CustomerOrderType:
        create_order_from_cart_mutation = CreateOrderFromCartMutation(self.graphql_client)

        variables = {"command": payload}

        result = create_order_from_cart_mutation.execute(variables=variables, return_fields=ORDER_FRAGMENT)

        return result

    def remove_cart_address(self, payload: InputRemoveCartAddressType) -> CartType:
        remove_cart_address_mutation = RemoveCartAddressMutation(self.graphql_client)

        variables = {"command": payload}

        result = remove_cart_address_mutation.execute(variables=variables, return_fields=CART_FRAGMENT)

        return result

    def clear_cart(self, payload: InputClearCartType) -> CartType:
        clear_cart_mutation = ClearCartMutation(self.graphql_client)

        variables = {"command": payload}

        result = clear_cart_mutation.execute(variables=variables, return_fields=CART_FRAGMENT)

        return result

    def clear_payments(self, payload: InputClearPaymentsType) -> CartType:
        clear_payments_mutation = ClearPaymentsMutation(self.graphql_client)

        variables = {"command": payload}

        result = clear_payments_mutation.execute(variables=variables, return_fields=CART_FRAGMENT)

        return result

    def clear_shipments(self, payload: InputClearShipmentsType) -> CartType:
        clear_shipments_mutation = ClearShipmentsMutation(self.graphql_client)

        variables = {"command": payload}

        result = clear_shipments_mutation.execute(variables=variables, return_fields=CART_FRAGMENT)

        return result

    def remove_cart(self, payload: InputRemoveCartType) -> None:
        remove_cart_mutation = RemoveCartMutation(self.graphql_client)

        variables = {"command": payload}

        result = remove_cart_mutation.execute(variables=variables, return_fields=None)

        return result

    def apply_coupon(self, payload: InputAddCouponType) -> CartType:
        add_coupon_mutation = AddCouponMutation(self.graphql_client)

        variables = {"command": payload}

        result = add_coupon_mutation.execute(variables=variables, return_fields=CART_FRAGMENT)

        return result

    def remove_coupon(self, payload: InputRemoveCouponType) -> CartType:
        remove_coupon_mutation = RemoveCouponMutation(self.graphql_client)

        variables = {"command": payload}

        result = remove_coupon_mutation.execute(variables=variables, return_fields=CART_FRAGMENT)

        return result
