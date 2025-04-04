from gql import gql
from graphql_requests.graphql_import_resolver import resolve_imports


cart_fragment = resolve_imports("cart_fragment.graphql")

REMOVE_CART_ADDRESS = gql(
    f"""
    {cart_fragment}

    mutation removeCartAddress($command: InputRemoveCartAddressType!) {{
        removeCartAddress(command: $command) {{
            ...CartFragment
        }}
    }}
    """
)
