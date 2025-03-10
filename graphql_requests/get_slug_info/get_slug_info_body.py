from gql import gql

GET_SLUG_INFO = gql(
    """
    query GetSlugInfo($storeId: String!, $cultureName: String!, $slug: String!) {
        slugInfo(
            storeId: $storeId
            cultureName: $cultureName
            slug: $slug
        ) {
            slug
            objectId
            objectType
            semanticUrl
            __typename
        }
    }
"""
)
