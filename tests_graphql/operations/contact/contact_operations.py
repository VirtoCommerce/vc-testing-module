from gql import Client
from graphql_client.mutations.request_registration import RequestRegistrationMutation
from graphql_client.mutations.delete_contact import DeleteContactMutation
from graphql_client.types.input_request_registration_type import InputRequestRegistrationType
from graphql_client.types.request_registration_type import RequestRegistrationType
from graphql_client.types.input_delete_contact_type import InputDeleteContactType


class ContactOperations:
    def __init__(self, auth_token: str, graphql_client: Client):
        self.auth_token = auth_token
        self.graphql_client = graphql_client

    def create_contact(self, payload: InputRequestRegistrationType) -> RequestRegistrationType:
        request_registration_mutation = RequestRegistrationMutation(self.graphql_client)

        variables = {"command": payload}

        return_fields = """
            result {
                succeeded
            }
            account {
                id
                username
                email
                status
            }
            contact {
                id
                firstName
                lastName
                status
            }
            organization {
                id
                name
                status
            }
        """

        result = request_registration_mutation.execute(variables=variables, return_fields=return_fields)

        return result

    def delete_contact(self, payload: InputDeleteContactType) -> None:
        self.graphql_client.set_headers({"Authorization": f"Bearer {self.auth_token}"})

        delete_contact_mutation = DeleteContactMutation(self.graphql_client)

        variables = {"command": payload}

        result = delete_contact_mutation.execute(variables=variables, return_fields=None)

        return result
