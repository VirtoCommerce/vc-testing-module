from gql import gql
from graphql_client.types.string_connection import StringConnection


class SettingValuesQuery:
    def __init__(self, graphql_client):
        self.graphql_client = graphql_client

    def execute(self, variables: dict, return_fields: str = None) -> StringConnection:
        query_string = f"""
            query settingValues($after: String, $first: Int, $name: String) {{
                settingValues(
                    after: $after,
                    first: $first,
                    name: $name
                ) {{
                    {return_fields}
                }}
            }}
        """

        return self.graphql_client.execute(gql(query_string), variables)["settingValues"]
