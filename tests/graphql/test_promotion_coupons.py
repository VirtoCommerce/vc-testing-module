import allure
import pytest
from core.clients import GraphQLClient
from gql.operations import PromotionCouponOperations
from tests.constants import PERCENTAGE_COUPON_CODE
from tests.context import Context

_USERNAME = "acme_store_employee_1@acme.com"
_PERCENTAGE_LOCALIZED_LABEL = "10% Off - en"
_END_DATED_COUPON_CODE = "SPRING15"
_END_DATE_YEAR = "2030"


@pytest.mark.graphql
@pytest.mark.with_user(_USERNAME)
@allure.feature("Account / Coupons (GraphQL)")
@allure.title("promotionCoupons returns the store's public promotion coupons")
def test_promotion_coupons_returns_store_coupons(graphql_client: GraphQLClient, ctx: Context) -> None:
    ops = PromotionCouponOperations(client=graphql_client)
    coupons = ops.get_promotion_coupons(
        store_id=ctx.store_id, user_id=ctx.user_id, culture_name=ctx.culture_name, first=100
    )

    with allure.step("Every returned coupon exposes a code and a label"):
        assert coupons
        assert all(c.coupon_code for c in coupons)
        assert all(c.label for c in coupons)

    with allure.step(f"The seeded coupon '{PERCENTAGE_COUPON_CODE}' is present"):
        codes = {c.coupon_code.upper() for c in coupons}
        assert PERCENTAGE_COUPON_CODE.upper() in codes


@pytest.mark.graphql
@pytest.mark.with_user(_USERNAME)
@allure.feature("Account / Coupons (GraphQL)")
@allure.title("promotionCoupons resolves the coupon's localized label")
def test_promotion_coupons_localized_label(graphql_client: GraphQLClient, ctx: Context) -> None:
    ops = PromotionCouponOperations(client=graphql_client)
    coupons = ops.get_promotion_coupons(
        store_id=ctx.store_id, user_id=ctx.user_id, culture_name=ctx.culture_name, first=100
    )

    coupon = next((c for c in coupons if c.coupon_code.upper() == PERCENTAGE_COUPON_CODE.upper()), None)
    assert coupon is not None, f"'{PERCENTAGE_COUPON_CODE}' was not returned by promotionCoupons"

    with allure.step("The localized (en-US) label is returned, distinct from the promotion name"):
        assert coupon.label == _PERCENTAGE_LOCALIZED_LABEL
        assert coupon.label != coupon.name


@pytest.mark.graphql
@pytest.mark.with_user(_USERNAME)
@allure.feature("Account / Coupons (GraphQL)")
@allure.title("promotionCoupons returns a promotion's end date when one is set")
def test_promotion_coupons_end_date(graphql_client: GraphQLClient, ctx: Context) -> None:
    ops = PromotionCouponOperations(client=graphql_client)
    coupons = ops.get_promotion_coupons(
        store_id=ctx.store_id, user_id=ctx.user_id, culture_name=ctx.culture_name, first=100
    )

    coupon = next((c for c in coupons if c.coupon_code.upper() == _END_DATED_COUPON_CODE.upper()), None)
    assert coupon is not None, f"'{_END_DATED_COUPON_CODE}' was not returned by promotionCoupons"

    with allure.step(f"The end date is an ISO datetime in {_END_DATE_YEAR}"):
        assert coupon.end_date is not None
        assert coupon.end_date.startswith(_END_DATE_YEAR)
