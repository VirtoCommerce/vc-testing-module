from gql import gql
from graphql_requests.graphql_import_resolver import resolve_imports


cart_fragment = resolve_imports("cart_fragment.graphql")

CART = gql(
    f"""
    {cart_fragment}

    query Cart($storeId: String!, $userId: String!, $currencyCode: String!, $cultureName: String) {{
        cart(
            storeId: $storeId
            userId: $userId
            currencyCode: $currencyCode
            cultureName: $cultureName
        ) {{
            ...CartFragment
        }}
    }}
    """
)
