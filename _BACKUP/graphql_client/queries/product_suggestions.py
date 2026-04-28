from gql import gql
from graphql_client.types.product_suggestions_query_response_type import ProductSuggestionsQueryResponseType


class ProductSuggestionsQuery:
    def __init__(self, graphql_client):
        self.graphql_client = graphql_client

    def execute(self, variables: dict, return_fields: str = None) -> ProductSuggestionsQueryResponseType:
        query_string = f"""
            query productSuggestions($storeId: String!, $query: String, $size: Int) {{
                productSuggestions(
                    storeId: $storeId,
                    query: $query,
                    size: $size
                ) {{
                    {return_fields}
                }}
            }}
        """

        return self.graphql_client.execute(gql(query_string), variables)["productSuggestions"]
