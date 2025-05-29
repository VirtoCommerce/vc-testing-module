from gql import Client
from graphql_client.mutations.delete_users import DeleteUsersMutation
from graphql_client.queries.me import MeQuery
from graphql_client.types.user_type import UserType
from graphql_client.types.input_delete_user_type import InputDeleteUserType
from graphql_client.types.identity_result_type import IdentityResultType


class UserOperations:
    def __init__(self, graphql_client: Client):
        self.graphql_client = graphql_client

    def get_user(self, user_id: str = None) -> UserType:
        me_query = MeQuery(self.graphql_client)

        variables = {"userId": user_id}

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

        result = me_query.execute(variables=variables, return_fields=return_fields)

        return result

    def delete_users(self, payload: InputDeleteUserType) -> IdentityResultType:
        delete_users_mutation = DeleteUsersMutation(self.graphql_client)

        variables = {"command": payload}

        return_fields = """
            succeeded
        """

        result = delete_users_mutation.execute(variables=variables, return_fields=return_fields)

        return result
