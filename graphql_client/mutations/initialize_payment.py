from gql import gql
from graphql_client.types.initialize_payment_result_type import InitializePaymentResultType


class InitializePaymentMutation:
    def __init__(self, graphql_client):
        self.graphql_client = graphql_client

    def execute(self, variables: dict, return_fields: str = None) -> InitializePaymentResultType:
        query_string = f"""
            mutation initializePayment($command: InputInitializePaymentType!) {{
                initializePayment(
                    command: $command
                ) {{
                    {return_fields}
                }}
            }}
        """

        return self.graphql_client.execute(gql(query_string), variables)["initializePayment"]
