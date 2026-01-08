from gql import gql
from graphql_client.types.initialize_cart_payment_result_type import InitializeCartPaymentResultType


class InitializeCartPaymentMutation:
    def __init__(self, graphql_client):
        self.graphql_client = graphql_client

    def execute(self, variables: dict, return_fields: str = None) -> InitializeCartPaymentResultType:
        query_string = f"""
            mutation initializeCartPayment($command: InputInitializeCartPaymentType!) {{
                initializeCartPayment(
                    command: $command
                ) {{
                    {return_fields}
                }}
            }}
        """

        return self.graphql_client.execute(gql(query_string), variables)["initializeCartPayment"]
