from gql import gql

GET_ME = gql(
    """
    query GetMe($storeId: String!, $userId: String!, $cultureName: String) {
        me(
            storeId: $storeId
            userId: $userId
            cultureName: $cultureName
        ) {
            id
            userName
            email
            firstName
            lastName
            middleName
            fullName
            phoneNumber
            addresses {
                id
                name
                firstName
                lastName
                email
                organization
                countryCode
                countryName
                regionId
                regionName
                city
                line1
                line2
                postalCode
                phone
                isDefault
                __typename
            }
            __typename
        }
    }
"""
)
