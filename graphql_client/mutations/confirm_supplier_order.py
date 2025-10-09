from gql import gql
from graphql_client.types.result_type import ResultType


class ConfirmSupplierOrderMutation:
    def __init__(self, graphql_client):
        self.graphql_client = graphql_client

    def execute(self, variables: dict, return_fields: str = None) -> ResultType:
        query_string = f"""
            mutation confirmSupplierOrder($command: InputConfirmSupplierOrderType!) {{
                confirmSupplierOrder(
                    command: $command
                ) {{
                    {return_fields}
                }}
            }}
        """

        return self.graphql_client.execute(gql(query_string), variables)["confirmSupplierOrder"]
