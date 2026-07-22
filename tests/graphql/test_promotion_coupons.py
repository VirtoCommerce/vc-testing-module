import allure
import pytest
from core.clients import GraphQLClient
from gql.operations import PromotionCouponOperations
from tests.constants import EXPIRED_COUPON_CODE, PERCENTAGE_COUPON_CODE
from tests.context import Context

_USERNAME = "acme_store_employee_1@acme.com"


@pytest.mark.graphql
@pytest.mark.with_user(_USERNAME)
@allure.feature("Account / Coupons (GraphQL)")
@allure.title("Promotion coupons query returns active store coupons")
def test_promotion_coupons_returns_items(graphql_client: GraphQLClient, ctx: Context) -> None:
    ops = PromotionCouponOperations(client=graphql_client)

    with allure.step("Query promotion coupons for the store"):
        coupons = ops.get_promotion_coupons(
            store_id=ctx.store_id,
            user_id=ctx.user_id,
            culture_name=ctx.culture_name,
            first=100,
        )

    with allure.step("At least one coupon is returned and every item has a code"):
        assert coupons
        assert all(c.coupon_code for c in coupons)

    with allure.step(f"The active coupon '{PERCENTAGE_COUPON_CODE}' is present"):
        codes = {c.coupon_code.upper() for c in coupons}
        assert PERCENTAGE_COUPON_CODE.upper() in codes


@pytest.mark.graphql
@pytest.mark.with_user(_USERNAME)
@allure.feature("Account / Coupons (GraphQL)")
@allure.title("Expired coupon is absent from the promotion coupons list")
def test_promotion_coupons_expired_absent(graphql_client: GraphQLClient, ctx: Context) -> None:
    # Depends on the promotionCoupons resolver filtering out coupons whose
    # expiration date has passed (server-side). This is the behaviour under
    # regression: the seeded QAEXPIRED coupon is past-dated, so it must not be
    # returned. If a backend is observed to skip expiry filtering (some demo
    # backends have shown async/filtering surprises), this will fail loudly by
    # design rather than being silently weakened to a no-op.
    ops = PromotionCouponOperations(client=graphql_client)

    with allure.step("Query promotion coupons for the store"):
        coupons = ops.get_promotion_coupons(
            store_id=ctx.store_id,
            user_id=ctx.user_id,
            culture_name=ctx.culture_name,
            first=100,
        )

    with allure.step(f"The expired coupon '{EXPIRED_COUPON_CODE}' is not returned"):
        codes = {c.coupon_code.upper() for c in coupons}
        assert EXPIRED_COUPON_CODE.upper() not in codes
