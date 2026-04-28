from gql import gql
from graphql_client.types.dynamic_property_type import DynamicPropertyType


class DynamicPropertyQuery:
    def __init__(self, graphql_client):
        self.graphql_client = graphql_client

    def execute(self, variables: dict, return_fields: str = None) -> DynamicPropertyType:
        query_string = f"""
            query dynamicProperty($idOrName: String!, $cultureName: String, $objectType: String) {{
                dynamicProperty(
                    idOrName: $idOrName,
                    cultureName: $cultureName,
                    objectType: $objectType
                ) {{
                    {return_fields}
                }}
            }}
        """

        return self.graphql_client.execute(gql(query_string), variables)["dynamicProperty"]
