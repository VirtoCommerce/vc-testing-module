from gql import gql
from graphql_client.types.prices_sum_type import PricesSumType


class PricesSumQuery:
    def __init__(self, graphql_client):
        self.graphql_client = graphql_client

    def execute(self, variables: dict, return_fields: str = None) -> PricesSumType:
        query_string = f"""
            query pricesSum($cartId: String!, $storeId: String!, $currencyCode: String!, $cultureName: String, $userId: String, $lineItemIds: [String]!) {{
                pricesSum(
                    cartId: $cartId,
                    storeId: $storeId,
                    currencyCode: $currencyCode,
                    cultureName: $cultureName,
                    userId: $userId,
                    lineItemIds: $lineItemIds
                ) {{
                    {return_fields}
                }}
            }}
        """

        return self.graphql_client.execute(gql(query_string), variables)["pricesSum"]
