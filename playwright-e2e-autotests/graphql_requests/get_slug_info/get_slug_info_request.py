import allure
from .get_slug_info_body import GET_SLUG_INFO


class GetSlugInfoRequest:
    def __init__(self, graphql_client):
        self.client = graphql_client

    @allure.step("Get slug info (GraphQL)")
    def execute(self, slug, store_id="", culture_name="en-US"):
        variables = {"storeId": store_id, "cultureName": culture_name, "slug": slug}
        result = self.client.execute(GET_SLUG_INFO, variable_values=variables)
        return result
