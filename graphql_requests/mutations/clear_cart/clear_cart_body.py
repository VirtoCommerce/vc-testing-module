from gql import gql
from graphql_requests.graphql_import_resolver import resolve_imports


cart_fragment = resolve_imports("cart_fragment.graphql")

CLEAR_CART = gql(
    f"""
    {cart_fragment}

    mutation ClearCart($command: InputClearCartType!) {{
        clearCart(command: $command) {{
            ...CartFragment
        }}
    }}
    """
)
