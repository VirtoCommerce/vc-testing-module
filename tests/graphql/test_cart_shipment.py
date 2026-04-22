import pytest
from core.clients import GraphQLClient
from gql.operations import CartOperations
from gql.types import ShipmentInput
from tests.constants import TEST_CART_ADDRESS
from tests.context import Context

from utils.address_utils import addresses_equal

_PRODUCT_ID = "smartphone-apple-iphone-17-256gb-mist-blue"
_QUANTITY = 3
_SHIPPING_METHOD = "FixedRate"
_GROUND_OPTION = ("Ground", 15.00)
_AIR_OPTION = ("Air", 25.00)


@pytest.mark.graphql
@pytest.mark.with_cart([(_PRODUCT_ID, _QUANTITY)])
def test_checkout_shipment(graphql_client: GraphQLClient, ctx: Context) -> None:
    cart_ops = CartOperations(client=graphql_client)

    shipment_input = ShipmentInput(
        shipment_method_code=_SHIPPING_METHOD,
        shipment_method_option=_GROUND_OPTION[0],
        price=_GROUND_OPTION[1],
        delivery_address=TEST_CART_ADDRESS,
    )
    cart = cart_ops.add_or_update_cart_shipment(
        store_id=ctx.store_id,
        user_id=ctx.user_id,
        culture_name=ctx.culture_name,
        currency_code=ctx.currency_code,
        shipment=shipment_input,
    )
    assert cart is not None
    assert cart.shipments is not None and len(cart.shipments) == 1

    shipment = cart.shipments[0]
    assert shipment.shipment_method_code == _SHIPPING_METHOD
    assert shipment.shipment_method_option == _GROUND_OPTION[0]
    assert shipment.price is not None and shipment.price.amount == _GROUND_OPTION[1]
    assert shipment.delivery_address is not None
    assert addresses_equal(a=shipment.delivery_address, b=TEST_CART_ADDRESS)

    updated_address = shipment.delivery_address.model_copy(update={"line1": "Change St 123"})
    shipment_input.id = shipment.id
    shipment_input.shipment_method_option = _AIR_OPTION[0]
    shipment_input.price = _AIR_OPTION[1]
    shipment_input.delivery_address = updated_address
    cart = cart_ops.add_or_update_cart_shipment(
        store_id=ctx.store_id,
        user_id=ctx.user_id,
        culture_name=ctx.culture_name,
        currency_code=ctx.currency_code,
        shipment=shipment_input,
    )
    assert cart.shipments is not None and len(cart.shipments) == 1

    shipment = cart.shipments[0]
    assert shipment.shipment_method_code == _SHIPPING_METHOD
    assert shipment.shipment_method_option == _AIR_OPTION[0]
    assert shipment.price is not None and shipment.price.amount == _AIR_OPTION[1]
    assert shipment.delivery_address is not None
    assert addresses_equal(a=shipment.delivery_address, b=updated_address)
