from gql import gql
from graphql_client.types.child_categories_query_response_type import ChildCategoriesQueryResponseType


class ChildCategoriesQuery:
    def __init__(self, graphql_client):
        self.graphql_client = graphql_client

    def execute(self, variables: dict, return_fields: str = None) -> ChildCategoriesQueryResponseType:
        query_string = f"""
            query childCategories($storeId: String!, $userId: String, $cultureName: String, $currencyCode: String, $previousOutline: String, $categoryId: String, $maxLevel: Int, $onlyActive: Boolean, $productFilter: String) {{
                childCategories(
                    storeId: $storeId,
                    userId: $userId,
                    cultureName: $cultureName,
                    currencyCode: $currencyCode,
                    previousOutline: $previousOutline,
                    categoryId: $categoryId,
                    maxLevel: $maxLevel,
                    onlyActive: $onlyActive,
                    productFilter: $productFilter
                ) {{
                    {return_fields}
                }}
            }}
        """

        return self.graphql_client.execute(gql(query_string), variables)["childCategories"]
