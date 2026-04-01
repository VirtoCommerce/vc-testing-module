from gql.operations.base_operations import BaseOperations, gql
from gql.types.identity_result import IdentityResult
from gql.types.user import User


class UserOperations(BaseOperations):
    def get_me(self) -> User | None:
        # fmt: off
        query = gql("""
            query GetMe {
              me {
                ...UserFragment
              }
            }
        """)
        # fmt: on
        result = self._client.execute(self._build_query(query))
        data = result["data"]["me"]
        return User.model_validate(data) if data else None

    def invite_user(
        self,
        store_id: str,
        emails: list[str],
        organization_id: str | None = None,
        role_ids: list[str] | None = None,
        url_suffix: str | None = None,
        message: str | None = None,
    ) -> IdentityResult:
        # fmt: off
        mutation = gql("""
            mutation InviteUser($command: InputInviteUserType!) {
              inviteUser(command: $command) {
                ...CustomIdentityResultFragment
              }
            }
        """)
        # fmt: on
        result = self._client.execute(
            self._build_query(mutation),
            variables={
                "command": {
                    "storeId": store_id,
                    "emails": emails,
                    **({"organizationId": organization_id} if organization_id else {}),
                    **({"roleIds": role_ids} if role_ids else {}),
                    **({"urlSuffix": url_suffix} if url_suffix else {}),
                    **({"message": message} if message else {}),
                }
            },
        )
        return IdentityResult.model_validate(result["data"]["inviteUser"])

    def delete_users(self, user_names: list[str]) -> IdentityResult:
        # fmt: off
        mutation = gql("""
            mutation DeleteUsers($command: InputDeleteUserType!) {
              deleteUsers(command: $command) {
                ...IdentityResultFragment
              }
            }
        """)
        # fmt: on
        result = self._client.execute(
            self._build_query(mutation),
            variables={"command": {"userNames": user_names}},
        )
        return IdentityResult.model_validate(result["data"]["deleteUsers"])
