from gql import gql
from graphql_requests.graphql_import_resolver import resolve_imports

cart_fragment = resolve_imports("cart_fragment.graphql")

UNSELECT_CART_ITEMS = gql(
    f"""
    {cart_fragment}

    mutation UnselectCartItems($command: InputChangeCartItemsSelectedType) {{
        unSelectCartItems(command: $command) {{
            ...CartFragment
        }}
    }}
    """
)
