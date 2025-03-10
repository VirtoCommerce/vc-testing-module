import allure
from .get_me_body import GET_ME


class GetMeRequest:
    def __init__(self, graphql_client):
        self.client = graphql_client

    @allure.step("Get me (GraphQL)")
    def execute(self, user_id, store_id="", culture_name="en-US"):
        variables = {
            "storeId": store_id,
            "userId": user_id,
            "cultureName": culture_name,
        }
        result = self.client.execute(GET_ME, variable_values=variables)
        return result
