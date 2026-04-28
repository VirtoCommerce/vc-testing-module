from gql import gql


class ValidateCouponQuery:
    def __init__(self, graphql_client):
        self.graphql_client = graphql_client

    def execute(self, variables: dict, return_fields: str = None) -> bool:
        query_string = f"""
            query validateCoupon($cartId: String, $storeId: String!, $currencyCode: String!, $userId: String!, $cultureName: String, $cartName: String, $cartType: String, $coupon: String!) {{
                validateCoupon(
                    cartId: $cartId,
                    storeId: $storeId,
                    currencyCode: $currencyCode,
                    userId: $userId,
                    cultureName: $cultureName,
                    cartName: $cartName,
                    cartType: $cartType,
                    coupon: $coupon
                )
            }}
        """

        return self.graphql_client.execute(gql(query_string), variables)["validateCoupon"]
