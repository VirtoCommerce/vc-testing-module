from gql import Client
from graphql_client.types.category_connection import CategoryConnection
from graphql_client.types.category import Category
from graphql_client.queries.categories import CategoriesQuery
from graphql_client.queries.category import CategoryQuery


class CategoriesOperations:
    def __init__(self, graphql_client: Client) -> None:
        self.graphql_client = graphql_client

    def get_categories(
        self,
        store_id: str,
        user_id: str,
        currency_code: str,
        culture_name: str,
        filter: str = None,
        category_ids: list[str] = None,
    ) -> CategoryConnection:
        categories_query = CategoriesQuery(self.graphql_client)

        variables = {
            "storeId": store_id,
            "userId": user_id,
            "currencyCode": currency_code,
            "cultureName": culture_name,
            "filter": filter,
            "categoryIds": category_ids,
        }

        return_fields = """
            totalCount
            items {
                id
                code
                name
            }
        """

        result = categories_query.execute(variables=variables, return_fields=return_fields)

        return result

    def get_category(self, store_id: str, user_id: str, currency_code: str, culture_name: str, id: str) -> Category:
        category_query = CategoryQuery(self.graphql_client)

        variables = {
            "storeId": store_id,
            "userId": user_id,
            "currencyCode": currency_code,
            "cultureName": culture_name,
            "id": id,
        }

        return_fields = """
            id
            code
            name
        """

        result = category_query.execute(variables=variables, return_fields=return_fields)

        return result
