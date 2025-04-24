from gql import gql
from graphql_client.types.dynamic_property_connection import DynamicPropertyConnection


class DynamicPropertiesQuery:
    def __init__(self, graphql_client):
        self.graphql_client = graphql_client

    def execute(self, variables: dict, return_fields: str = None) -> DynamicPropertyConnection:
        query_string = f"""
            query dynamicProperties($after: String, $first: Int, $cultureName: String, $filter: String, $sort: String, $objectType: String) {{
                dynamicProperties(
                    after: $after,
                    first: $first,
                    cultureName: $cultureName,
                    filter: $filter,
                    sort: $sort,
                    objectType: $objectType
                ) {{
                    {return_fields}
                }}
            }}
        """

        return self.graphql_client.execute(gql(query_string), variables)["dynamicProperties"]
