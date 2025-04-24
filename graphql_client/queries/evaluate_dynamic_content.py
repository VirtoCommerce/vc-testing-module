from gql import gql
from graphql_client.types.evaluate_dynamic_content_result_type import EvaluateDynamicContentResultType


class EvaluateDynamicContentQuery:
    def __init__(self, graphql_client):
        self.graphql_client = graphql_client

    def execute(self, variables: dict, return_fields: str = None) -> EvaluateDynamicContentResultType:
        query_string = f"""
            query evaluateDynamicContent($storeId: String, $placeName: String, $categoryId: String, $productId: String, $cultureName: String, $toDate: DateTime, $tags: [String], $userGroups: [String]) {{
                evaluateDynamicContent(
                    storeId: $storeId,
                    placeName: $placeName,
                    categoryId: $categoryId,
                    productId: $productId,
                    cultureName: $cultureName,
                    toDate: $toDate,
                    tags: $tags,
                    userGroups: $userGroups
                ) {{
                    {return_fields}
                }}
            }}
        """

        return self.graphql_client.execute(gql(query_string), variables)["evaluateDynamicContent"]
