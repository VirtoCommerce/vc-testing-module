from gql import Client
from graphql_requests.mutations.delete_users.delete_users_mutation import DeleteUsersMutation
from graphql_requests.queries.me.me_query import MeQuery


class UserOperations:
    def __init__(self, auth_token: str, graphql_client: Client):
        self.auth_token = auth_token
        self.graphql_client = graphql_client

    def get_me(self, user_id: str = None, auth_required: bool = False):
        """
        Get current user or user by id.
        Args:
            user_id (str, optional): ID of user to get. If not provided, returns current user.
            auth_required (bool, optional): Whether authentication is required. If True, uses admin credentials.
        Returns:
            dict: Response containing user data with fields like id and userName.
        """

        if auth_required:
            self.graphql_client.set_headers({"Authorization": f"Bearer {self.auth_token}"})

        me_query = MeQuery(self.graphql_client)

        result = me_query.execute(user_id)

        return result

    def delete_users(self, usernames: list[str]):
        """
        Delete users by their IDs.
        Args:
            usernames (list[str]): List of usernames to delete.
        Returns:
            dict: Response containing success status and any errors.
        """

        self.graphql_client.set_headers({"Authorization": f"Bearer {self.auth_token}"})

        delete_users_mutation = DeleteUsersMutation(self.graphql_client)

        result = delete_users_mutation.execute(usernames)

        return result
