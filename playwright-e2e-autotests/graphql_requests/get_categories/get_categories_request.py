import allure
from .get_categories_body import GET_CATEGORIES


class GetCategoriesRequest:
    def __init__(self, graphql_client):
        self.client = graphql_client

    @allure.step("Get categories (GraphQL)")
    def execute(self, store_id="", culture_name="en-US"):
        variables = {"storeId": store_id, "cultureName": culture_name}
        result = self.client.execute(GET_CATEGORIES, variable_values=variables)
        return result
