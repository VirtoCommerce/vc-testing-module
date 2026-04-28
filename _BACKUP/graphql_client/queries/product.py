from gql import gql
from graphql_client.types.product import Product


class ProductQuery:
    def __init__(self, graphql_client):
        self.graphql_client = graphql_client

    def execute(self, variables: dict, return_fields: str = None) -> Product:
        query_string = f"""
            query product($id: String!, $storeId: String!, $userId: String, $currencyCode: String, $cultureName: String, $previousOutline: String, $custom: String) {{
                product(
                    id: $id,
                    storeId: $storeId,
                    userId: $userId,
                    currencyCode: $currencyCode,
                    cultureName: $cultureName,
                    previousOutline: $previousOutline,
                    custom: $custom
                ) {{
                    {return_fields}
                }}
            }}
        """

        return self.graphql_client.execute(gql(query_string), variables)["product"]
