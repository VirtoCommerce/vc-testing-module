from gql import gql
from graphql_client.types.brand_type import BrandType


class BrandQuery:
    def __init__(self, graphql_client):
        self.graphql_client = graphql_client

    def execute(self, variables: dict, return_fields: str = None) -> BrandType:
        query_string = f"""
            query brand($id: String!, $storeId: String!, $cultureName: String) {{
                brand(
                    id: $id,
                    storeId: $storeId,
                    cultureName: $cultureName
                ) {{
                    {return_fields}
                }}
            }}
        """

        return self.graphql_client.execute(gql(query_string), variables)["brand"]
