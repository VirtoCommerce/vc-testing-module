import allure
import pytest
from core.clients import GraphQLClient
from gql.operations import CartOperations
from gql.types import PaymentInput
from tests.constants import TEST_CART_ADDRESS
from tests.context import Context

from utils.address_utils import addresses_equal

_PRODUCT_ID = "smartphone-apple-iphone-17-256gb-black"
_QUANTITY = 3
_DEFAULT_PAYMENT_METHOD = "DefaultManualPaymentMethod"
_AUTHORIZE_NET_PAYMENT_METHOD = "AuthorizeNetPaymentMethod"


@pytest.mark.graphql
@pytest.mark.with_cart([(_PRODUCT_ID, _QUANTITY)])
@allure.feature("Cart / Payment (GraphQL)")
@allure.title("Add and update payment method on cart")
def test_checkout_payment(graphql_client: GraphQLClient, ctx: Context) -> None:
    cart_ops = CartOperations(client=graphql_client)

    payment_input = PaymentInput(
        payment_gateway_code=_DEFAULT_PAYMENT_METHOD, billing_address=TEST_CART_ADDRESS
    )

    with allure.step(f"Add payment method {_DEFAULT_PAYMENT_METHOD} to cart"):
        cart = cart_ops.add_or_update_cart_payment(
            store_id=ctx.store_id,
            user_id=ctx.user_id,
            culture_name=ctx.culture_name,
            currency_code=ctx.currency_code,
            payment=payment_input,
        )

    with allure.step(
        f"Verify payment {_DEFAULT_PAYMENT_METHOD} and billing address are set"
    ):
        assert cart is not None
        assert cart.payments is not None and len(cart.payments) == 1

        payment = cart.payments[0]
        assert payment.payment_gateway_code == _DEFAULT_PAYMENT_METHOD
        assert payment.billing_address is not None
        assert addresses_equal(a=payment.billing_address, b=TEST_CART_ADDRESS)

    updated_address = payment.billing_address.model_copy(
        update={"line1": "Change St 123"}
    )
    payment_input.id = payment.id
    payment_input.payment_gateway_code = _AUTHORIZE_NET_PAYMENT_METHOD
    payment_input.billing_address = updated_address

    with allure.step(
        f"Update payment to {_AUTHORIZE_NET_PAYMENT_METHOD} with new billing address"
    ):
        cart = cart_ops.add_or_update_cart_payment(
            store_id=ctx.store_id,
            user_id=ctx.user_id,
            culture_name=ctx.culture_name,
            currency_code=ctx.currency_code,
            payment=payment_input,
        )

    with allure.step(
        f"Verify payment is updated to {_AUTHORIZE_NET_PAYMENT_METHOD} with new address"
    ):
        assert cart.payments is not None and len(cart.payments) == 1

        payment = cart.payments[0]
        assert payment.payment_gateway_code == _AUTHORIZE_NET_PAYMENT_METHOD
        assert addresses_equal(a=payment.billing_address, b=updated_address)
