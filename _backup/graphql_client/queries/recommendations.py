from gql import gql
from graphql_client.types.get_recommendations_response_type import GetRecommendationsResponseType


class RecommendationsQuery:
    def __init__(self, graphql_client):
        self.graphql_client = graphql_client

    def execute(self, variables: dict, return_fields: str = None) -> GetRecommendationsResponseType:
        query_string = f"""
            query recommendations($storeId: String!, $userId: String, $cultureName: String, $currencyCode: String, $previousOutline: String, $productId: String, $model: String, $fallbackProductsFilter: String, $maxRecommendations: Int) {{
                recommendations(
                    storeId: $storeId,
                    userId: $userId,
                    cultureName: $cultureName,
                    currencyCode: $currencyCode,
                    previousOutline: $previousOutline,
                    productId: $productId,
                    model: $model,
                    fallbackProductsFilter: $fallbackProductsFilter,
                    maxRecommendations: $maxRecommendations
                ) {{
                    {return_fields}
                }}
            }}
        """

        return self.graphql_client.execute(gql(query_string), variables)["recommendations"]
