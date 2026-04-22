from gql import gql
from graphql_client.types.property import Property


class PropertyQuery:
    def __init__(self, graphql_client):
        self.graphql_client = graphql_client

    def execute(self, variables: dict, return_fields: str = None) -> Property:
        query_string = f"""
            query property($id: String!, $cultureName: String) {{
                property(
                    id: $id,
                    cultureName: $cultureName
                ) {{
                    {return_fields}
                }}
            }}
        """

        return self.graphql_client.execute(gql(query_string), variables)["property"]
