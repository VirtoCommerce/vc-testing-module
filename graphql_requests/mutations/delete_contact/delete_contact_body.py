from gql import gql


DELETE_CONTACT = gql(
    """
    mutation DeleteContact($command: InputDeleteContactType!) {
        deleteContact(command: $command)
    }
    """
)
