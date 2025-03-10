from gql import gql

GET_CATEGORIES = gql(
    """
    query GetCategories($storeId: String!, $cultureName: String) {
        categories(
            storeId: $storeId
            cultureName: $cultureName
        ) {
            items {
                id
                name
                slug
                parent {
                    id
                    name
                    slug
                    __typename
                }
                __typename
            }
            totalCount
            __typename
        }
    }
"""
)
