import pytest

from core.clients import GraphQLClient
from gql.operations import CartOperations
from gql.types import Cart, PaymentInput, ShipmentInput
from tests.constants import TEST_CART_ADDRESS
from tests.context import Context

_PRODUCT_ID = "product-acme-laptop-asus-zenbook-a14-ux3407"
_QUANTITY = 2
_PAYMENT_METHOD = "DefaultManualPaymentMethod"
_SHIPPING_METHOD = "FixedRate"
_SHIPPING_OPTION = "Ground"
_SHIPPING_PRICE = 15.00


@pytest.mark.graphql
@pytest.mark.with_cart([(_PRODUCT_ID, _QUANTITY)])
def test_cart_create_order(
    graphql_client: GraphQLClient, ctx: Context, with_cart: Cart
) -> None:
    cart_ops = CartOperations(client=graphql_client)

    cart_ops.add_or_update_cart_payment(
        store_id=ctx.store_id,
        user_id=ctx.user_id,
        payment=PaymentInput(
            payment_gateway_code=_PAYMENT_METHOD,
            billing_address=TEST_CART_ADDRESS,
        ),
    )
    cart_ops.add_or_update_cart_shipment(
        store_id=ctx.store_id,
        user_id=ctx.user_id,
        shipment=ShipmentInput(
            shipment_method_code=_SHIPPING_METHOD,
            shipment_method_option=_SHIPPING_OPTION,
            price=_SHIPPING_PRICE,
            delivery_address=TEST_CART_ADDRESS,
        ),
        currency_code=ctx.currency_code,
        culture_name=ctx.culture_name,
    )

    order = cart_ops.create_order_from_cart(cart_id=with_cart.id)

    assert order is not None
    assert order.number is not None

    assert len(order.items) == 1
    item = order.items[0]
    assert item.product_id == _PRODUCT_ID
    assert item.quantity == _QUANTITY

    assert len(order.in_payments) == 1
    payment = order.in_payments[0]
    assert payment.gateway_code == _PAYMENT_METHOD

    assert len(order.shipments) == 1
    shipment = order.shipments[0]
    assert shipment.shipment_method_code == _SHIPPING_METHOD
    assert shipment.shipment_method_option == _SHIPPING_OPTION
