from gql import gql
from graphql_client.types.back_in_stock_subscription_connection import BackInStockSubscriptionConnection


class BackInStockSubscriptionsQuery:
    def __init__(self, graphql_client):
        self.graphql_client = graphql_client

    def execute(self, variables: dict, return_fields: str = None) -> BackInStockSubscriptionConnection:
        query_string = f"""
            query backInStockSubscriptions($after: String, $first: Int, $keyword: String, $sort: String, $storeId: String, $productIds: [String], $isActive: Boolean) {{
                backInStockSubscriptions(
                    after: $after,
                    first: $first,
                    keyword: $keyword,
                    sort: $sort,
                    storeId: $storeId,
                    productIds: $productIds,
                    isActive: $isActive
                ) {{
                    {return_fields}
                }}
            }}
        """

        return self.graphql_client.execute(gql(query_string), variables)["backInStockSubscriptions"]
