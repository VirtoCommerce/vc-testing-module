from gql import Client
from graphql_requests.mutations.delete_contact.delete_contact_mutation import DeleteContactMutation
from graphql_requests.mutations.request_registration.request_registration_mutation import RequestRegistrationMutation


class ContactOperations:
    def __init__(self, auth_token: str, graphql_client: Client):
        self.auth_token = auth_token
        self.graphql_client = graphql_client

    def create_contact(
        self, store_id: str, email: str, password: str, first_name: str, last_name: str, organization_name: str = None
    ):
        """
        Create a new contact by registering a user.
        Args:
            store_id (str): ID of the store
            email (str): Email address for the contact/account
            password (str): Password for the account
            first_name (str): Contact's first name
            last_name (str): Contact's last name
            organization_name (str, optional): Name of organization if creating an organization contact
        Returns:
            dict: Response containing the created contact, account and organization (if specified) data
        """

        request_registration_mutation = RequestRegistrationMutation(self.graphql_client)

        result = request_registration_mutation.execute(
            store_id=store_id,
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name,
            organization_name=organization_name,
        )

        return result

    def delete_contact(self, contact_id: str) -> bool:
        """
        Delete a contact by ID.
        Args:
            contact_id (str): ID of the contact to delete
        Returns:
            bool: True if deletion was successful
        """

        self.graphql_client.set_headers({"Authorization": f"Bearer {self.auth_token}"})

        delete_contact_mutation = DeleteContactMutation(self.graphql_client)

        result = delete_contact_mutation.execute(contact_id)

        return result
