from gql import gql
from graphql_client.types.loyalty_operation_log_connection import LoyaltyOperationLogConnection


class LoyaltyPointsHistoryQuery:
    def __init__(self, graphql_client):
        self.graphql_client = graphql_client

    def execute(self, variables: dict, return_fields: str = None) -> LoyaltyOperationLogConnection:
        query_string = f"""
            query loyaltyPointsHistory($after: String, $first: Int, $keyword: String, $sort: String, $userId: String, $operationType: String) {{
                loyaltyPointsHistory(
                    after: $after,
                    first: $first,
                    keyword: $keyword,
                    sort: $sort,
                    userId: $userId,
                    operationType: $operationType
                ) {{
                    {return_fields}
                }}
            }}
        """

        return self.graphql_client.execute(gql(query_string), variables)["loyaltyPointsHistory"]
