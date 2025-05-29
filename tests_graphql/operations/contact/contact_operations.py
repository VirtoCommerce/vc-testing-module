from gql import Client
from graphql_client.mutations.request_registration import RequestRegistrationMutation
from graphql_client.mutations.delete_contact import DeleteContactMutation
from graphql_client.types.input_request_registration_type import InputRequestRegistrationType
from graphql_client.types.request_registration_type import RequestRegistrationType
from graphql_client.types.input_delete_contact_type import InputDeleteContactType
from graphql_client.queries.organization import OrganizationQuery
from graphql_client.types.organization import Organization


class ContactOperations:
    def __init__(self, graphql_client: Client):
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
        delete_contact_mutation = DeleteContactMutation(self.graphql_client)

        variables = {"command": payload}

        result = delete_contact_mutation.execute(variables=variables, return_fields=None)

        return result

    def fetch_organization_contacts(
        self, organization_id: str, user_id: str, search_phrase: str = None
    ) -> Organization:
        organization_query = OrganizationQuery(self.graphql_client)

        variables = {"id": organization_id, "userId": user_id}

        return_fields = f"""
            id
            name
            contacts(
                searchPhrase: \"{search_phrase if search_phrase else ''}\"
                sort: \"name:asc\"
            ) {{
                totalCount
                items {{
                    id
                    name
                    firstName
                    lastName
                    emails
                    status
                    securityAccounts {{
                        userName
                        roles {{
                            id
                            name
                        }}
                    }}
                }}
            }}
        """

        result = organization_query.execute(variables=variables, return_fields=return_fields)

        return result
