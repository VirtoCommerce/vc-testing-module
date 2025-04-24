from gql import gql


class CanLeaveFeedbackQuery:
    def __init__(self, graphql_client):
        self.graphql_client = graphql_client

    def execute(self, variables: dict, return_fields: str = None) -> bool:
        query_string = f"""
            query canLeaveFeedback($storeId: String!, $entityId: String!, $entityType: String!) {{
                canLeaveFeedback(
                    storeId: $storeId,
                    entityId: $entityId,
                    entityType: $entityType
                )
            }}
        """

        return self.graphql_client.execute(gql(query_string), variables)["canLeaveFeedback"]
