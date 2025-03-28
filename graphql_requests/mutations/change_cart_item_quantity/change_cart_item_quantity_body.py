from gql import gql
from graphql_requests.graphql_import_resolver import resolve_imports


cart_fragment = resolve_imports("cart_fragment.graphql")

CHANGE_CART_ITEM_QUANTITY = gql(
    f"""
    {cart_fragment}

    mutation ChangeCartItemQuantity($command: InputChangeCartItemQuantityType!) {{
        changeCartItemQuantity(command: $command) {{
            ...CartFragment
        }}
    }}
    """
)
