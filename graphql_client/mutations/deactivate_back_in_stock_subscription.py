from gql import gql
from graphql_client.types.back_in_stock_subscription_type import BackInStockSubscriptionType


class DeactivateBackInStockSubscriptionMutation:
    def __init__(self, graphql_client):
        self.graphql_client = graphql_client

    def execute(self, variables: dict, return_fields: str = None) -> BackInStockSubscriptionType:
        query_string = f"""
            mutation deactivateBackInStockSubscription($command: DeactivateBackInStockSubscriptionCommandType!) {{
                deactivateBackInStockSubscription(
                    command: $command
                ) {{
                    {return_fields}
                }}
            }}
        """

        return self.graphql_client.execute(gql(query_string), variables)["deactivateBackInStockSubscription"]
