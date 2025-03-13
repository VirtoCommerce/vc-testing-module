from gql import gql

REQUEST_REGISTRATION = gql(
    """
    mutation RequestRegistration($command: InputRequestRegistrationType!) {
        requestRegistration(command: $command) {
            account {
                id
            }
            organization {
                id
            }
            contact {
                id
            }
            result {
                succeeded
                errors {
                    code
                }
            }
        }
    }
    """
)