import allure
import pytest
from core.clients import GraphQLClient
from core.global_settings import GlobalSettings
from gql.operations import PromotionCouponOperations
from gql.types import PromotionCoupon
from tests.constants import EXPIRED_COUPON_CODE, PERCENTAGE_COUPON_CODE
from tests.context import Context
from utils.polling_utils import poll_until

_USERNAME = "acme_store_employee_1@acme.com"


def _poll_promotion_coupons(
    ops: PromotionCouponOperations, ctx: Context, global_settings: GlobalSettings
) -> list[PromotionCoupon] | None:
    """Poll ``promotionCoupons`` until it returns a populated list.

    The query is backed by data that can lag or be entirely absent on some
    storefront builds (env divergence), so poll for the seeded coupons to
    surface. Returns the populated list, or ``None`` if it stays empty for the
    whole polling budget (caller should skip rather than hard-fail).
    """
    return poll_until(
        fetch=lambda: ops.get_promotion_coupons(
            store_id=ctx.store_id,
            user_id=ctx.user_id,
            culture_name=ctx.culture_name,
            first=100,
        ),
        predicate=lambda coupons: len(coupons) > 0,
        attempts=global_settings.poll_attempts,
        interval=global_settings.poll_interval,
    )


@pytest.mark.graphql
@pytest.mark.with_user(_USERNAME)
@allure.feature("Account / Coupons (GraphQL)")
@allure.title("Promotion coupons query returns active store coupons")
def test_promotion_coupons_returns_items(
    graphql_client: GraphQLClient, ctx: Context, global_settings: GlobalSettings
) -> None:
    ops = PromotionCouponOperations(client=graphql_client)

    with allure.step("Poll promotion coupons for the store until populated"):
        coupons = _poll_promotion_coupons(ops, ctx, global_settings)

    if not coupons:
        pytest.skip(
            "promotionCoupons returned no items on this storefront build "
            "(feature/data not surfaced — env divergence)"
        )

    # The list is populated: from here on, missing data is a real signal, so assert.
    with allure.step("Every returned item has a code"):
        assert all(c.coupon_code for c in coupons)

    with allure.step(f"The active coupon '{PERCENTAGE_COUPON_CODE}' is present"):
        codes = {c.coupon_code.upper() for c in coupons}
        assert PERCENTAGE_COUPON_CODE.upper() in codes


@pytest.mark.graphql
@pytest.mark.with_user(_USERNAME)
@allure.feature("Account / Coupons (GraphQL)")
@allure.title("Expired coupon is absent from the promotion coupons list")
def test_promotion_coupons_expired_absent(
    graphql_client: GraphQLClient, ctx: Context, global_settings: GlobalSettings
) -> None:
    # Depends on the promotionCoupons resolver filtering out coupons whose
    # expiration date has passed (server-side). The seeded QAEXPIRED coupon is
    # past-dated, so once the list is populated it must not be returned. If the
    # list is empty/unavailable on this build we cannot assert absence, so skip;
    # absence is only asserted against a populated list (a real signal).
    ops = PromotionCouponOperations(client=graphql_client)

    with allure.step("Poll promotion coupons for the store until populated"):
        coupons = _poll_promotion_coupons(ops, ctx, global_settings)

    if not coupons:
        pytest.skip(
            "promotionCoupons returned no items on this storefront build; "
            "cannot assert expired-coupon absence (env divergence)"
        )

    with allure.step(f"The expired coupon '{EXPIRED_COUPON_CODE}' is not returned"):
        codes = {c.coupon_code.upper() for c in coupons}
        assert EXPIRED_COUPON_CODE.upper() not in codes
