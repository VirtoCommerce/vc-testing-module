from gql import gql
from graphql_client.types.approve_quote_result_type import ApproveQuoteResultType


class ApproveQuoteRequestMutation:
    def __init__(self, graphql_client):
        self.graphql_client = graphql_client

    def execute(self, variables: dict, return_fields: str = None) -> ApproveQuoteResultType:
        query_string = f"""
            mutation approveQuoteRequest($command: ApproveQuoteCommandType!) {{
                approveQuoteRequest(
                    command: $command
                ) {{
                    {return_fields}
                }}
            }}
        """

        return self.graphql_client.execute(gql(query_string), variables)["approveQuoteRequest"]
