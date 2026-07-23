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
@allure.title("promotionCoupons returns store coupons with resolved labels and end dates")
def test_promotion_coupons_returns_store_coupons(graphql_client: GraphQLClient, ctx: Context) -> None:
    ops = PromotionCouponOperations(client=graphql_client)
    coupons = ops.get_promotion_coupons(
        store_id=ctx.store_id, user_id=ctx.user_id, culture_name=ctx.culture_name, first=100
    )

    with allure.step(f"Every coupon exposes a code and a label, and '{PERCENTAGE_COUPON_CODE}' is present"):
        assert coupons
        assert all(c.coupon_code for c in coupons)
        assert all(c.label for c in coupons)
        codes = {c.coupon_code.upper() for c in coupons}
        assert PERCENTAGE_COUPON_CODE.upper() in codes

    with allure.step(f"'{PERCENTAGE_COUPON_CODE}' resolves its localized (en-US) label, distinct from the name"):
        percentage = next((c for c in coupons if c.coupon_code.upper() == PERCENTAGE_COUPON_CODE.upper()), None)
        assert percentage is not None, f"'{PERCENTAGE_COUPON_CODE}' was not returned by promotionCoupons"
        assert percentage.label == _PERCENTAGE_LOCALIZED_LABEL
        assert percentage.label != percentage.name

    with allure.step(f"'{_END_DATED_COUPON_CODE}' returns an end date (ISO datetime in {_END_DATE_YEAR})"):
        end_dated = next((c for c in coupons if c.coupon_code.upper() == _END_DATED_COUPON_CODE.upper()), None)
        assert end_dated is not None, f"'{_END_DATED_COUPON_CODE}' was not returned by promotionCoupons"
        assert end_dated.end_date is not None
        assert end_dated.end_date.startswith(_END_DATE_YEAR)


@pytest.mark.graphql
@pytest.mark.with_user(_USERNAME)
@allure.feature("Account / Coupons (GraphQL)")
@allure.title("promotionCoupons honors the first limit and the name sort order")
def test_promotion_coupons_pagination_and_sort(graphql_client: GraphQLClient, ctx: Context) -> None:
    ops = PromotionCouponOperations(client=graphql_client)
    all_coupons = ops.get_promotion_coupons(
        store_id=ctx.store_id, user_id=ctx.user_id, culture_name=ctx.culture_name, first=100
    )
    if len(all_coupons) < 2:
        pytest.skip("Need at least two public coupons to exercise pagination/sort")

    all_ids = {c.id for c in all_coupons}
    all_codes = {c.coupon_code for c in all_coupons}

    with allure.step("first=1 returns exactly one coupon drawn from the full set"):
        page = ops.get_promotion_coupons(
            store_id=ctx.store_id, user_id=ctx.user_id, culture_name=ctx.culture_name, first=1
        )
        assert len(page) == 1
        assert page[0].id in all_ids

    # Verified live: the backend sorts on the promotion `name` field. asc/desc
    # produce a deterministic ordering that is the exact reverse of one another
    # (other keys such as `couponCode`/`code`/`label` are silently ignored).
    with allure.step("Sorting by name asc and desc yields exact reverses of one another"):
        asc = ops.get_promotion_coupons(
            store_id=ctx.store_id, user_id=ctx.user_id, culture_name=ctx.culture_name, first=100, sort="name:asc"
        )
        desc = ops.get_promotion_coupons(
            store_id=ctx.store_id, user_id=ctx.user_id, culture_name=ctx.culture_name, first=100, sort="name:desc"
        )
        asc_codes = [c.coupon_code for c in asc]
        desc_codes = [c.coupon_code for c in desc]

        assert set(asc_codes) == all_codes
        assert set(desc_codes) == all_codes
        assert asc_codes == list(reversed(desc_codes))
        assert asc_codes != desc_codes

    # NOTE: `after` (cursor paging) is not asserted here — get_promotion_coupons
    # returns only the items list and discards totalCount/pageInfo, so there is
    # no end cursor to feed back in. Covering `after` cleanly would require
    # extending the operation's return shape, which is out of scope for this PR.


@pytest.mark.graphql
@allure.feature("Account / Coupons (GraphQL)")
@allure.title("promotionCoupons denies anonymous access")
def test_promotion_coupons_anonymous_denied(graphql_client: GraphQLClient, ctx: Context) -> None:
    ops = PromotionCouponOperations(client=graphql_client)

    # Verified live: with no `with_user` marker the ctx is anonymous, and the
    # backend rejects promotionCoupons outright with a GraphQL "Unauthorized"
    # error ("Anonymous access denied..."). The query requires authentication —
    # so guests are barred server-side, not merely hidden by the storefront UI.
    with allure.step("Anonymous promotionCoupons raises an Unauthorized GraphQL error"):
        with pytest.raises(ValueError, match="(?i)anonymous access denied|unauthorized"):
            ops.get_promotion_coupons(
                store_id=ctx.store_id, user_id=ctx.user_id, culture_name=ctx.culture_name, first=100
            )
