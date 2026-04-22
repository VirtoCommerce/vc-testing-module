from gql import Client

from graphql_client.mutations.add_address_to_favorites import (
    AddAddressToFavoritesMutation,
)
from graphql_client.mutations.change_organization_contact_role import (
    ChangeOrganizationContactRoleMutation,
)
from graphql_client.mutations.delete_contact import DeleteContactMutation
from graphql_client.mutations.delete_member_addresses import (
    DeleteMemberAddressesMutation,
)
from graphql_client.mutations.invite_user import InviteUserMutation
from graphql_client.mutations.lock_organization_contact import (
    LockOrganizationContactMutation,
)
from graphql_client.mutations.remove_address_from_favorites import (
    RemoveAddressFromFavoritesMutation,
)
from graphql_client.mutations.remove_member_from_organization import (
    RemoveMemberFromOrganizationMutation,
)
from graphql_client.mutations.request_registration import RequestRegistrationMutation
from graphql_client.mutations.unlock_organization_contact import (
    UnlockOrganizationContactMutation,
)
from graphql_client.mutations.update_contact import UpdateContactMutation
from graphql_client.mutations.update_member_addresses import (
    UpdateMemberAddressesMutation,
)
from graphql_client.queries.organization import OrganizationQuery
from graphql_client.types.add_address_to_favorites_command_type import (
    AddAddressToFavoritesCommandType,
)
from graphql_client.types.contact_type import ContactType
from graphql_client.types.custom_identity_result_type import CustomIdentityResultType
from graphql_client.types.input_change_organization_contact_role_type import (
    InputChangeOrganizationContactRoleType,
)
from graphql_client.types.input_delete_contact_type import InputDeleteContactType
from graphql_client.types.input_delete_member_address_type import (
    InputDeleteMemberAddressType,
)
from graphql_client.types.input_invite_user_type import InputInviteUserType
from graphql_client.types.input_lock_unlock_organization_contact_type import (
    InputLockUnlockOrganizationContactType,
)
from graphql_client.types.input_remove_member_from_organization_type import (
    InputRemoveMemberFromOrganizationType,
)
from graphql_client.types.input_request_registration_type import (
    InputRequestRegistrationType,
)
from graphql_client.types.input_update_contact_type import InputUpdateContactType
from graphql_client.types.input_update_member_address_type import (
    InputUpdateMemberAddressType,
)
from graphql_client.types.member_type import MemberType
from graphql_client.types.organization import Organization
from graphql_client.types.remove_address_from_favorites_command_type import (
    RemoveAddressFromFavoritesCommandType,
)
from graphql_client.types.request_registration_type import RequestRegistrationType
from graphql_operations.common.address_fragment import ADDRESS_FRAGMENT


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

    def fetch_organization_addresses(self, organization_id: str, user_id: str) -> Organization:
        organization_query = OrganizationQuery(self.graphql_client)

        variables = {"id": organization_id, "userId": user_id}

        return_fields = f"""
            id
            name
            addresses {{
                items {{
                    {ADDRESS_FRAGMENT}
                    isFavorite
                }}
            }}
        """

        result = organization_query.execute(variables=variables, return_fields=return_fields)

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
                        id
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

    def lock_organization_contact(self, payload: InputLockUnlockOrganizationContactType) -> ContactType:
        lock_organization_contact_mutation = LockOrganizationContactMutation(self.graphql_client)

        variables = {"command": payload}

        return_fields = """
            id
            name
            status
        """

        result = lock_organization_contact_mutation.execute(variables=variables, return_fields=return_fields)

        return result

    def unlock_organization_contact(self, payload: InputLockUnlockOrganizationContactType) -> ContactType:
        unlock_organization_contact_mutation = UnlockOrganizationContactMutation(self.graphql_client)

        variables = {"command": payload}

        return_fields = """
            id
            name
            status
        """

        result = unlock_organization_contact_mutation.execute(variables=variables, return_fields=return_fields)

        return result

    def change_organization_contact_role(
        self, payload: InputChangeOrganizationContactRoleType
    ) -> CustomIdentityResultType:
        change_organization_contact_role_mutation = ChangeOrganizationContactRoleMutation(self.graphql_client)

        variables = {"command": payload}

        return_fields = """
            succeeded
        """

        result = change_organization_contact_role_mutation.execute(variables=variables, return_fields=return_fields)

        return result

    def invite_user(self, payload: InputInviteUserType) -> CustomIdentityResultType:
        invite_user_mutation = InviteUserMutation(self.graphql_client)

        variables = {"command": payload}

        return_fields = f"""
            succeeded
            errors {{
                code
                description
            }}
        """

        result = invite_user_mutation.execute(variables=variables, return_fields=return_fields)

        return result

    def remove_contact_from_organization(self, payload: InputRemoveMemberFromOrganizationType) -> ContactType:
        remove_contact_from_organization_mutation = RemoveMemberFromOrganizationMutation(self.graphql_client)

        variables = {"command": payload}

        return_fields = """
            id
            name
            status
            organizationId
        """

        result = remove_contact_from_organization_mutation.execute(variables=variables, return_fields=return_fields)

        return result

    def update_contact_addresses(self, payload: InputUpdateMemberAddressType) -> MemberType:
        update_contact_addresses_mutation = UpdateMemberAddressesMutation(self.graphql_client)

        variables = {"command": payload}

        return_fields = f"""
            id
            addresses {{
                items {{{
                    ADDRESS_FRAGMENT
                }}}
            }}
        """

        result = update_contact_addresses_mutation.execute(variables=variables, return_fields=return_fields)

        return result

    def delete_contact_address(self, payload: InputDeleteMemberAddressType) -> MemberType:
        delete_contact_addresses_mutation = DeleteMemberAddressesMutation(self.graphql_client)

        variables = {"command": payload}

        return_fields = f"""
            id
            addresses {{
                items {{{
                    ADDRESS_FRAGMENT
                }}}
            }}
        """

        result = delete_contact_addresses_mutation.execute(variables=variables, return_fields=return_fields)

        return result

    def add_address_to_favorites(self, payload: AddAddressToFavoritesCommandType) -> bool:
        add_address_to_favorites_mutation = AddAddressToFavoritesMutation(self.graphql_client)

        variables = {"command": payload}

        result = add_address_to_favorites_mutation.execute(variables=variables)

        return result

    def remove_address_from_favorites(self, payload: RemoveAddressFromFavoritesCommandType) -> bool:
        remove_address_from_favorites_mutation = RemoveAddressFromFavoritesMutation(self.graphql_client)

        variables = {"command": payload}

        result = remove_address_from_favorites_mutation.execute(variables=variables)

        return result

    def update_contact(self, payload: InputUpdateContactType) -> ContactType:
        update_contact_mutation = UpdateContactMutation(self.graphql_client)

        variables = {"command": payload}

        result = update_contact_mutation.execute(variables=variables)

        return result
