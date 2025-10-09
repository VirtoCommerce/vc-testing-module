from gql import gql
from graphql_client.types.address_suggestion_response_type import AddressSuggestionResponseType


class AddressSuggestionsQuery:
    def __init__(self, graphql_client):
        self.graphql_client = graphql_client

    def execute(self, variables: dict, return_fields: str = None) -> AddressSuggestionResponseType:
        query_string = f"""
            query addressSuggestions($query: String!) {{
                addressSuggestions(
                    query: $query
                ) {{
                    {return_fields}
                }}
            }}
        """

        return self.graphql_client.execute(gql(query_string), variables)["addressSuggestions"]
