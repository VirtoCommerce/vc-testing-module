from gql import gql
from graphql_requests.graphql_import_resolver import resolve_imports


cart_fragment = resolve_imports("cart_fragment.graphql")

REMOVE_CART_ITEM = gql(
    f"""
    {cart_fragment}

    mutation RemoveCartItem($command: InputRemoveItemType!) {{
        removeCartItem(command: $command) {{
            ...CartFragment
        }}
    }}
    """
)
