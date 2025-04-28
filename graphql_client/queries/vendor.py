from gql import gql
from graphql_client.types.vendor import Vendor


class VendorQuery:
    def __init__(self, graphql_client):
        self.graphql_client = graphql_client

    def execute(self, variables: dict, return_fields: str = None) -> Vendor:
        query_string = f"""
            query vendor($id: String!, $userId: String) {{
                vendor(
                    id: $id,
                    userId: $userId
                ) {{
                    {return_fields}
                }}
            }}
        """

        return self.graphql_client.execute(gql(query_string), variables)["vendor"]
