from gql import gql
from graphql_client.types.customer_review import CustomerReview


class CreateCustomerReviewMutation:
    def __init__(self, graphql_client):
        self.graphql_client = graphql_client

    def execute(self, variables: dict, return_fields: str = None) -> CustomerReview:
        query_string = f"""
            mutation createCustomerReview($command: CreateCustomerReviewCommandType!) {{
                createCustomerReview(
                    command: $command
                ) {{
                    {return_fields}
                }}
            }}
        """

        return self.graphql_client.execute(gql(query_string), variables)["createCustomerReview"]
