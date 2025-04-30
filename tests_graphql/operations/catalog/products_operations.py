from gql import Client
from graphql_client.types.product_connection import ProductConnection
from graphql_client.types.product import Product
from graphql_client.queries.products import ProductsQuery
from graphql_client.queries.product import ProductQuery
from tests_graphql.operations.catalog.fragments.product_fragment import PRODUCT_FRAGMENT


class ProductsOperations:
    def __init__(self, graphql_client: Client):
        self.graphql_client = graphql_client

    def get_products(
        self, store_id: str, user_id: str, currency_code: str, culture_name: str, query: str = None, filter: str = None
    ) -> ProductConnection:
        products_query = ProductsQuery(self.graphql_client)

        variables = {
            "storeId": store_id,
            "userId": user_id,
            "currencyCode": currency_code,
            "cultureName": culture_name,
            "query": query,
            "filter": filter,
        }

        return_fields = f"""
            totalCount
            items {{
                {PRODUCT_FRAGMENT}
            }}
        """

        result = products_query.execute(variables=variables, return_fields=return_fields)

        return result

    def get_product(self, store_id: str, user_id: str, culture_name: str, currency_code: str, id: str) -> Product:
        product_query = ProductQuery(self.graphql_client)

        variables = {
            "storeId": store_id,
            "userId": user_id,
            "cultureName": culture_name,
            "currencyCode": currency_code,
            "id": id,
        }

        result = product_query.execute(variables=variables, return_fields=PRODUCT_FRAGMENT)

        return result
