from gql.types.promotion_coupon import PromotionCoupon

from .base_operations import BaseOperations, gql


class PromotionCouponOperations(BaseOperations):
    def get_promotion_coupons(
        self,
        store_id: str,
        user_id: str,
        culture_name: str,
        sort: str | None = None,
        first: int | None = None,
        after: str | None = None,
    ) -> list[PromotionCoupon]:
        # fmt: off
        query = gql("""
            query GetPromotionCoupons(
                $storeId: String!,
                $userId: String!,
                $cultureName: String!,
                $sort: String,
                $first: Int,
                $after: String,
            ) {
              promotionCoupons(
                storeId: $storeId,
                userId: $userId,
                cultureName: $cultureName,
                sort: $sort,
                first: $first,
                after: $after,
              ) {
                totalCount
                items {
                  ...PromotionCouponFragment
                }
              }
            }
        """)
        # fmt: on
        result = self._client.execute(
            self._build_query(query),
            variables={
                "storeId": store_id,
                "userId": user_id,
                "cultureName": culture_name,
                "sort": sort,
                "first": first,
                "after": after,
            },
        )
        items = result["data"]["promotionCoupons"]["items"] or []
        return [PromotionCoupon.model_validate(item) for item in items]
