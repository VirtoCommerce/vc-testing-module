from gql import gql
from graphql_client.types.contact_connection import ContactConnection


class ContactsQuery:
    def __init__(self, graphql_client):
        self.graphql_client = graphql_client

    def execute(self, variables: dict, return_fields: str = None) -> ContactConnection:
        query_string = f"""
            query contacts($after: String, $first: Int, $searchPhrase: String, $sort: String) {{
                contacts(
                    after: $after,
                    first: $first,
                    searchPhrase: $searchPhrase,
                    sort: $sort
                ) {{
                    {return_fields}
                }}
            }}
        """

        return self.graphql_client.execute(gql(query_string), variables)["contacts"]
