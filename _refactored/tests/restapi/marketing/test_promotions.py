"""Promotions and coupons — migrated from Katalon `API Coverage/ModuleMarketing/PromoAndCoupons/*`.

Katalon scripts:
  promoCreate                    → test_promo_create
  promoUpdate                    → test_promo_update
  promoUpdate_AlternativeWay     → test_promo_update_alt
  promoDelete                    → test_promo_delete
  promoCoupon_createUpdateDelete → test_coupon_create_search_delete
  promo_CreateTestData           → test_promo_create_test_data (create promo + add coupon)
"""

import uuid

import allure
import pytest

from restapi.operations import CouponOperations, PromotionOperations


@pytest.mark.restapi
@allure.feature("Marketing / Promotions (REST API)")
@allure.title("Create promotion")
def test_promo_create(make_promotion) -> None:
    with allure.step("POST /api/marketing/promotions"):
        promo = make_promotion()

    with allure.step("Verify"):
        assert promo["id"]
        assert promo["name"].startswith("QAPromo_")


@pytest.mark.restapi
@allure.feature("Marketing / Promotions (REST API)")
@allure.title("Get new promotion template")
def test_promo_get_new(promo_ops: PromotionOperations) -> None:
    with allure.step("GET /api/marketing/promotions/new"):
        template = promo_ops.get_new()

    with allure.step("Verify template"):
        assert template is not None


@pytest.mark.restapi
@allure.feature("Marketing / Promotions (REST API)")
@allure.title("Get promotion by id")
def test_promo_get_by_id(make_promotion, promo_ops: PromotionOperations) -> None:
    promo = make_promotion()

    with allure.step(f"GET /api/marketing/promotions/{promo['id']}"):
        reloaded = promo_ops.get_by_id(promo["id"])

    assert reloaded["id"] == promo["id"]


@pytest.mark.restapi
@allure.feature("Marketing / Promotions (REST API)")
@allure.title("Search promotions")
def test_promo_search(make_promotion, promo_ops: PromotionOperations) -> None:
    promo = make_promotion()

    with allure.step("POST /api/marketing/promotions/search"):
        result = promo_ops.search()

    with allure.step("Verify"):
        assert result is not None
        items = result.get("results", []) if isinstance(result, dict) else result or []
        assert len(items) >= 1


@pytest.mark.restapi
@allure.feature("Marketing / Promotions (REST API)")
@allure.title("Update promotion — rename")
def test_promo_update(make_promotion, promo_ops: PromotionOperations) -> None:
    promo = make_promotion()
    new_name = f"{promo['name']}_UPD_{uuid.uuid4().hex[:4]}"

    with allure.step(f"PUT /api/marketing/promotions — name={new_name}"):
        promo_ops.update(promo, name=new_name)

    with allure.step("Verify"):
        reloaded = promo_ops.get_by_id(promo["id"])
        assert reloaded["name"] == new_name


@pytest.mark.restapi
@allure.feature("Marketing / Promotions (REST API)")
@allure.title("Update promotion — alternative way (description)")
def test_promo_update_alt(make_promotion, promo_ops: PromotionOperations) -> None:
    promo = make_promotion()
    desc = f"Updated desc {uuid.uuid4().hex[:6]}"

    with allure.step("PUT /api/marketing/promotions — description"):
        promo_ops.update(promo, description=desc)

    with allure.step("Verify"):
        reloaded = promo_ops.get_by_id(promo["id"])
        assert reloaded.get("description") == desc


@pytest.mark.restapi
@allure.feature("Marketing / Promotions (REST API)")
@allure.title("Delete promotion")
def test_promo_delete(promo_ops: PromotionOperations) -> None:
    promo = promo_ops.create(name=f"QADelPromo_{uuid.uuid4().hex[:8]}")

    with allure.step(f"DELETE /api/marketing/promotions?ids={promo['id']}"):
        promo_ops.delete(promo["id"])


@pytest.mark.restapi
@allure.feature("Marketing / Coupons (REST API)")
@allure.title("Coupon full lifecycle: create → search → update → get-by-id → delete → verify gone")
def test_coupon_create_update_delete(make_promotion, coupon_ops: CouponOperations) -> None:
    promo = make_promotion()
    code = f"QA-COUPON-{uuid.uuid4().hex[:6].upper()}"

    with allure.step("POST /api/marketing/promotions/coupons/add — create coupon"):
        coupon_ops.add([{"promotionId": promo["id"], "code": code, "maxUsesNumber": 15, "maxUsesPerUser": 10}])

    with allure.step("POST /api/marketing/promotions/coupons/search — locate by code"):
        search = coupon_ops.search(promotion_id=promo["id"])
        results = search.get("results", []) if isinstance(search, dict) else search or []
        found = next((c for c in results if c.get("code") == code), None)
        assert found is not None, f"Coupon {code} not found after create"
        assert found["maxUsesNumber"] == 15
        assert found["maxUsesPerUser"] == 10
        coupon_id = found["id"]

    updated_code = f"{code}-UPD"
    with allure.step("POST /coupons/add — update fields (same id, new code + counts)"):
        coupon_ops.add(
            [
                {
                    "id": coupon_id,
                    "promotionId": promo["id"],
                    "code": updated_code,
                    "maxUsesNumber": 17,
                    "maxUsesPerUser": 12,
                }
            ]
        )

    with allure.step(f"GET /coupons/{coupon_id} — verify update persisted"):
        reloaded = coupon_ops.get_by_id(coupon_id)
        assert reloaded["code"] == updated_code
        assert reloaded["maxUsesNumber"] == 17
        assert reloaded["maxUsesPerUser"] == 12

    with allure.step(f"DELETE /coupons/delete?ids={coupon_id}"):
        coupon_ops.delete(coupon_id)

    with allure.step("POST /coupons/search — verify coupon is gone"):
        post = coupon_ops.search(promotion_id=promo["id"])
        post_results = post.get("results", []) if isinstance(post, dict) else post or []
        assert not any(c.get("id") == coupon_id for c in post_results), "Deleted coupon still visible in search"


@pytest.mark.restapi
@allure.feature("Marketing / Coupons (REST API)")
@allure.title("Create, search, and delete coupon")
def test_coupon_create_search_delete(make_promotion, coupon_ops: CouponOperations) -> None:
    promo = make_promotion()
    coupon_code = f"QA-COUPON-{uuid.uuid4().hex[:6].upper()}"

    with allure.step("POST /api/marketing/promotions/coupons/add"):
        coupon_ops.add([{"promotionId": promo["id"], "code": coupon_code, "maxUsesNumber": 10}])

    with allure.step("POST /api/marketing/promotions/coupons/search"):
        search = coupon_ops.search(promotion_id=promo["id"])
        coupons = search.get("results", []) if isinstance(search, dict) else search or []
        found = next((c for c in coupons if c.get("code") == coupon_code), None)
        assert found is not None, f"Coupon {coupon_code} not found"

    with allure.step(f"DELETE /api/marketing/promotions/coupons/delete?ids={found['id']}"):
        coupon_ops.delete(found["id"])


@pytest.mark.restapi
@allure.feature("Marketing / Promotions (REST API)")
@allure.title("Create promotion with coupon (test data flow)")
def test_promo_create_test_data(make_promotion, coupon_ops: CouponOperations, promo_ops: PromotionOperations) -> None:
    promo = make_promotion()
    coupon_code = f"QA-DATA-{uuid.uuid4().hex[:6].upper()}"

    with allure.step("Add coupon to promotion"):
        coupon_ops.add([{"promotionId": promo["id"], "code": coupon_code, "maxUsesNumber": 5}])

    with allure.step("Verify promotion has coupon"):
        search = coupon_ops.search(promotion_id=promo["id"])
        coupons = search.get("results", []) if isinstance(search, dict) else search or []
        assert len(coupons) >= 1

    with allure.step("Cleanup coupons"):
        for c in coupons:
            try:
                coupon_ops.delete(c["id"])
            except Exception:
                pass
