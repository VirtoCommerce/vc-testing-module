from gql import gql
from graphql_client.types.category import Category


class CategoryQuery:
    def __init__(self, graphql_client):
        self.graphql_client = graphql_client

    def execute(self, variables: dict, return_fields: str = None) -> Category:
        query_string = f"""
            query category($id: String!, $storeId: String!, $userId: String, $currencyCode: String, $cultureName: String, $previousOutline: String) {{
                category(
                    id: $id,
                    storeId: $storeId,
                    userId: $userId,
                    currencyCode: $currencyCode,
                    cultureName: $cultureName,
                    previousOutline: $previousOutline
                ) {{
                    {return_fields}
                }}
            }}
        """

        return self.graphql_client.execute(gql(query_string), variables)["category"]
