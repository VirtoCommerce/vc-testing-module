from gql import gql
from graphql_requests.graphql_import_resolver import resolve_imports

cart_fragment = resolve_imports("cart_fragment.graphql")

SELECT_ALL_CART_ITEMS = gql(
    f"""
    {cart_fragment}

    mutation SelectAllCartItems($command: InputChangeAllCartItemsSelectedType!) {{
        selectAllCartItems(command: $command) {{
            ...CartFragment
        }}
    }}
    """
)
