import allure

from .request_registration_body import REQUEST_REGISTRATION

class RequestRegistrationRequest:
    def __init__(self, graphql_client):
        self.client = graphql_client

    @allure.step("Request registration (GraphQL)")
    def execute(
        self,
        store_id,
        email,
        password,
        first_name,
        last_name,
        organization_name
    ):
        variables = {
            "command": {
                "storeId": store_id,
                "account": {
                    "username": email,
                    "password": password,
                    "email": email,
                },
                "contact": {
                    "firstName": first_name,
                    "lastName": last_name
                },
                "organization": {
                    "name": organization_name
                }
            }
        }

        result = self.client.execute(REQUEST_REGISTRATION, variable_values=variables)

        return result
