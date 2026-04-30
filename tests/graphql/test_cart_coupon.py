import allure
import pytest
from core.clients import GraphQLClient
from gql.operations import CartOperations
from tests.context import Context

_PRODUCT_ID = "smartphone-apple-iphone-17-256gb-black"
_QUANTITY = 3
_COUPON_CODE = "COUPON-100-OFF"


@pytest.mark.graphql
@pytest.mark.with_cart([(_PRODUCT_ID, _QUANTITY)])
@allure.feature("Cart / Coupons (GraphQL)")
@allure.title("Add and remove a coupon on the cart")
def test_cart_coupon(graphql_client: GraphQLClient, ctx: Context) -> None:
    cart_ops = CartOperations(client=graphql_client)

    with allure.step(f"Add coupon {_COUPON_CODE} to cart"):
        cart = cart_ops.add_coupon(
            store_id=ctx.store_id,
            user_id=ctx.user_id,
            culture_name=ctx.culture_name,
            currency_code=ctx.currency_code,
            code=_COUPON_CODE,
        )

    with allure.step(f"Verify coupon {_COUPON_CODE} is applied successfully"):
        assert cart is not None
        assert cart.coupons is not None and len(cart.coupons) == 1

        coupon = cart.coupons[0]
        assert coupon.code == _COUPON_CODE
        assert coupon.is_applied_successfully == True

    with allure.step(f"Remove coupon {_COUPON_CODE} from cart"):
        cart = cart_ops.remove_coupon(
            store_id=ctx.store_id,
            user_id=ctx.user_id,
            culture_name=ctx.culture_name,
            currency_code=ctx.currency_code,
            code=_COUPON_CODE,
        )

    with allure.step("Verify cart has no coupons"):
        assert cart is not None
        assert cart.coupons is not None and len(cart.coupons) == 0
