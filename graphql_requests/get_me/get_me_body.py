from gql import gql

GET_ME = gql(
    """
query GetMe($userId: String) {
  me(userId: $userId) {
    id
    memberId
    userName
    email
    emailConfirmed
    photoUrl
    phoneNumber
    permissions
    isAdministrator
    passwordExpired
    passwordExpiryInDays
    forcePasswordChange
    lockedState
    contact {
      id
      firstName
      lastName
      fullName
      organizationId
      defaultLanguage
      currencyCode
      organizations {
        items {
          id
          name
          __typename
        }
        __typename
      }
      __typename
    }
    operator {
      userName
      contact {
        fullName
        __typename
      }
      __typename
    }
    roles {
      name
      __typename
    }
    __typename
  }
}
    """
)
