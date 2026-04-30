import allure
import pytest
from core.clients import GraphQLClient
from gql.operations import CartOperations
from gql.types.cart import Cart
from gql.types.shipment_input import ShipmentInput
from tests.context import Context

_PRODUCT_ID = "smartphone-apple-iphone-17-256gb-black"
_USERNAME = "acme_store_employee_1@acme.com"

_SHIPMENT_CASES = [
    ("BuyOnlinePickupInStore", "Pickup", 0.0),
    ("FixedRate", "Ground", 15.0),
    ("FixedRate", "Air", 25.0),
]


@pytest.mark.graphql
@pytest.mark.parametrize("method_code,method_option,price", _SHIPMENT_CASES)
@pytest.mark.with_user(_USERNAME)
@pytest.mark.with_cart([(_PRODUCT_ID, 1)])
@allure.feature("Checkout / Shipment Cost (GraphQL)")
@allure.title("Cart shipping total reflects selected shipment method price")
def test_checkout_shipment_cost(
    graphql_client: GraphQLClient,
    ctx: Context,
    with_cart: Cart,
    method_code: str,
    method_option: str | None,
    price: float | None,
) -> None:
    with allure.step("Verify initial shipping total is zero"):
        assert with_cart.shipping_total.amount == 0.0

    with allure.step(f"Apply shipment {method_code}/{method_option} (price={price})"):
        cart = CartOperations(client=graphql_client).add_or_update_cart_shipment(
            store_id=ctx.store_id,
            user_id=ctx.user_id,
            cart_id=with_cart.id,
            currency_code=ctx.currency_code,
            culture_name=ctx.culture_name,
            shipment=ShipmentInput(
                shipment_method_code=method_code,
                shipment_method_option=method_option,
                price=price,
            ),
        )

    with allure.step(f"Verify cart shipping total equals {price or 0.0}"):
        assert cart.shipping_total.amount == (price or 0.0)
