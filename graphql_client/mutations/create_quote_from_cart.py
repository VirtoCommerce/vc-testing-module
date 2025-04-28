from gql import gql
from graphql_client.types.quote_type import QuoteType


class CreateQuoteFromCartMutation:
    def __init__(self, graphql_client):
        self.graphql_client = graphql_client

    def execute(self, variables: dict, return_fields: str = None) -> QuoteType:
        query_string = f"""
            mutation createQuoteFromCart($command: CreateQuoteFromCartCommandType!) {{
                createQuoteFromCart(
                    command: $command
                ) {{
                    {return_fields}
                }}
            }}
        """

        return self.graphql_client.execute(gql(query_string), variables)["createQuoteFromCart"]
