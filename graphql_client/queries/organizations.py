from gql import gql
from graphql_client.types.organization_connection import OrganizationConnection


class OrganizationsQuery:
    def __init__(self, graphql_client):
        self.graphql_client = graphql_client

    def execute(self, variables: dict, return_fields: str = None) -> OrganizationConnection:
        query_string = f"""
            query organizations($after: String, $first: Int, $searchPhrase: String, $sort: String) {{
                organizations(
                    after: $after,
                    first: $first,
                    searchPhrase: $searchPhrase,
                    sort: $sort
                ) {{
                    {return_fields}
                }}
            }}
        """

        return self.graphql_client.execute(gql(query_string), variables)["organizations"]
