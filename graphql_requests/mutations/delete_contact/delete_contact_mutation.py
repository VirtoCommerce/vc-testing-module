from gql import Client
from .delete_contact_body import DELETE_CONTACT


class DeleteContactMutation:
    def __init__(self, graphql_client: Client):
        self.graphql_client = graphql_client

    def execute(self, contact_id: str) -> bool:
        variables = {"command": {"contactId": contact_id}}

        result: bool = self.client.execute(DELETE_CONTACT, variable_values=variables)

        return result
