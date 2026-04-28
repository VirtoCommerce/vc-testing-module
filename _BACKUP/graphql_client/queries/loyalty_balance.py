from gql import gql
from graphql_client.types.loyalty_balance_result import LoyaltyBalanceResult


class LoyaltyBalanceQuery:
    def __init__(self, graphql_client):
        self.graphql_client = graphql_client

    def execute(self, variables: dict, return_fields: str = None) -> LoyaltyBalanceResult:
        query_string = f"""
            query loyaltyBalance($userId: String, $orderId: String) {{
                loyaltyBalance(
                    userId: $userId,
                    orderId: $orderId
                ) {{
                    {return_fields}
                }}
            }}
        """

        return self.graphql_client.execute(gql(query_string), variables)["loyaltyBalance"]
