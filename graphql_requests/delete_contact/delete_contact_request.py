from .delete_contact_body import DELETE_CONTACT

class RequestDeleteContact:
    def __init__(self, graphql_client):
        self.client = graphql_client

    def execute(
        self,
        contact_id
    ):
        variables = {
            "command": {
                "contactId": contact_id
            }
        }

        result = self.client.execute(DELETE_CONTACT, variable_values=variables)

        return result
