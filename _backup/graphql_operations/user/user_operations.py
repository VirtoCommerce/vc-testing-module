from gql import Client

from graphql_client.mutations.delete_users import DeleteUsersMutation
from graphql_client.mutations.register_by_invitation import RegisterByInvitationMutation
from graphql_client.queries.me import MeQuery
from graphql_client.queries.user import UserQuery
from graphql_client.types.custom_identity_result_type import CustomIdentityResultType
from graphql_client.types.identity_result_type import IdentityResultType
from graphql_client.types.input_delete_user_type import InputDeleteUserType
from graphql_client.types.input_register_by_invitation_type import (
    InputRegisterByInvitationType,
)
from graphql_client.types.user_type import UserType


class UserOperations:
    def __init__(self, graphql_client: Client):
        self.graphql_client = graphql_client

    def get_user_by_username(self, username: str) -> UserType:
        user_query = UserQuery(self.graphql_client)

        variables = {"userName": username}

        return_fields = """
            id
            userName
            email
            roles {
                name
            }
            contact {
                id
                firstName
                lastName
                organizationId
            }
        """

        result = user_query.execute(variables=variables, return_fields=return_fields)

        return result

    def get_me(self) -> UserType:
        me_query = MeQuery(self.graphql_client)

        return_fields = """
            id
            userName
            email
            roles {
                name
            }
            contact {
                id
                name
                organizationId
            }
        """

        result = me_query.execute(variables={}, return_fields=return_fields)

        return result

    def delete_users(self, payload: InputDeleteUserType) -> IdentityResultType:
        delete_users_mutation = DeleteUsersMutation(self.graphql_client)

        variables = {"command": payload}

        return_fields = """
            succeeded
        """

        result = delete_users_mutation.execute(variables=variables, return_fields=return_fields)

        return result

    def register_by_invitation(self, payload: InputRegisterByInvitationType) -> CustomIdentityResultType:
        register_by_invitation_mutation = RegisterByInvitationMutation(self.graphql_client)

        variables = {"command": payload}

        return_fields = """
            succeeded
            errors {
                code
                description
            }
        """

        result = register_by_invitation_mutation.execute(variables=variables, return_fields=return_fields)

        return result
