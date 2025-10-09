from gql import gql
from graphql_client.types.supplier_type import SupplierType


class SupplierQuery:
    def __init__(self, graphql_client):
        self.graphql_client = graphql_client

    def execute(self, variables: dict, return_fields: str = None) -> SupplierType:
        query_string = f"""
            query supplier($id: String!) {{
                supplier(
                    id: $id
                ) {{
                    {return_fields}
                }}
            }}
        """

        return self.graphql_client.execute(gql(query_string), variables)["supplier"]
