from gql import gql


class ChangeOrderStatusMutation:
    def __init__(self, graphql_client):
        self.graphql_client = graphql_client

    def execute(self, variables: dict, return_fields: str = None) -> bool:
        query_string = f"""
            mutation changeOrderStatus($command: InputChangeOrderStatusType!) {{
                changeOrderStatus(
                    command: $command
                )
            }}
        """

        return self.graphql_client.execute(gql(query_string), variables)["changeOrderStatus"]
