from gql import gql
from graphql_client.types.create_quote_requests_result_type import CreateQuoteRequestsResultType


class CreateQuoteRequestsMutation:
    def __init__(self, graphql_client):
        self.graphql_client = graphql_client

    def execute(self, variables: dict, return_fields: str = None) -> CreateQuoteRequestsResultType:
        query_string = f"""
            mutation createQuoteRequests($command: InputCreateQuoteRequestsType!) {{
                createQuoteRequests(
                    command: $command
                ) {{
                    {return_fields}
                }}
            }}
        """

        return self.graphql_client.execute(gql(query_string), variables)["createQuoteRequests"]
