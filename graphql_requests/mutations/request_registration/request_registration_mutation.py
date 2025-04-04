from .request_registration_body import REQUEST_REGISTRATION


class RequestRegistrationMutation:
    def __init__(self, graphql_client):
        self.graphql_client = graphql_client

    def execute(
        self, store_id: str, email: str, password: str, first_name: str, last_name: str, organization_name: str = None
    ):
        variables = {
            "command": {
                "storeId": store_id,
                "account": {
                    "username": email,
                    "password": password,
                    "email": email,
                },
                "contact": {"firstName": first_name, "lastName": last_name},
            }
        }

        if organization_name:
            variables["command"]["organization"] = {"name": organization_name}

        result = self.graphql_client.execute(REQUEST_REGISTRATION, variable_values=variables)

        return result
