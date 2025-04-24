from gql import gql
from graphql_client.types.cart_type import CartType


class AddOrUpdateCartPaymentMutation:
    def __init__(self, graphql_client):
        self.graphql_client = graphql_client

    def execute(self, variables: dict, return_fields: str = None) -> CartType:
        query_string = f"""
            mutation addOrUpdateCartPayment($command: InputAddOrUpdateCartPaymentType!) {{
                addOrUpdateCartPayment(
                    command: $command
                ) {{
                    {return_fields}
                }}
            }}
        """

        return self.graphql_client.execute(gql(query_string), variables)["addOrUpdateCartPayment"]
