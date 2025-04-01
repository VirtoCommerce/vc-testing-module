from gql import gql
from graphql_requests.graphql_import_resolver import resolve_imports


cart_fragment = resolve_imports("cart_fragment.graphql")

ADD_ITEMS_CART = gql(
    f"""
    {cart_fragment}

    mutation AddItemsCart($command: InputAddItemsType!) {{
        addItemsCart(command: $command) {{
            ...CartFragment
        }}
    }}
    """
)
