import allure
from .authenticate_body import AUTHENTICATE


class AuthenticateRequest:
    def __init__(self, graphql_client):
        self.client = graphql_client

    @allure.step("Authenticate user (GraphQL)")
    def execute(self, username, password):
        variables = {"command": {"username": username, "password": password, "storeId": "B2B-store"}}
        result = self.client.execute(AUTHENTICATE, variable_values=variables)
        return result
