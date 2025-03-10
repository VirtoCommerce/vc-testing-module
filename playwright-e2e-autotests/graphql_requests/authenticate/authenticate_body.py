from gql import gql

AUTHENTICATE = gql(
    """
    mutation Authenticate($command: InputAuthenticateType!) {
        authenticate(command: $command) {
            userId
            userName
            accessToken
            refreshToken
            expiresIn
            tokenType
            passwordExpired
            passwordExpiryInDays
            forcePasswordChange
            lockedState
            __typename
        }
    }
"""
)
