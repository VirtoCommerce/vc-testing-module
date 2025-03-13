from gql import gql

DELETE_USERS = gql(
    """
    mutation DeleteUsers($command: InputDeleteUserType!) {
        deleteUsers(command: $command) {
            succeeded
            errors {
                code
                description
            }
        }
    }
    """
)