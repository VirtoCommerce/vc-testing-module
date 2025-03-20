from .request_registration_body import REQUEST_REGISTRATION


class RequestRegistrationRequest:
    def __init__(self, graphql_client):
        self.graphql_client = graphql_client

    def execute(self, store_id, email, password, first_name, last_name, organization_name=None):
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
