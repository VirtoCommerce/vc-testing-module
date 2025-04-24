from gql import gql
from graphql_client.types.create_review_result import CreateReviewResult


class CreateReviewMutation:
    def __init__(self, graphql_client):
        self.graphql_client = graphql_client

    def execute(self, variables: dict, return_fields: str = None) -> CreateReviewResult:
        query_string = f"""
            mutation createReview($command: CreateReviewCommandType!) {{
                createReview(
                    command: $command
                ) {{
                    {return_fields}
                }}
            }}
        """

        return self.graphql_client.execute(gql(query_string), variables)["createReview"]
