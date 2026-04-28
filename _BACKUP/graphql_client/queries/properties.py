from gql import gql
from graphql_client.types.property_connection import PropertyConnection


class PropertiesQuery:
    def __init__(self, graphql_client):
        self.graphql_client = graphql_client

    def execute(self, variables: dict, return_fields: str = None) -> PropertyConnection:
        query_string = f"""
            query properties($after: String, $first: Int, $storeId: String!, $types: [PropertyType], $filter: String, $cultureName: String) {{
                properties(
                    after: $after,
                    first: $first,
                    storeId: $storeId,
                    types: $types,
                    filter: $filter,
                    cultureName: $cultureName
                ) {{
                    {return_fields}
                }}
            }}
        """

        return self.graphql_client.execute(gql(query_string), variables)["properties"]
