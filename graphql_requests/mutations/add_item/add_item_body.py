from gql import gql
from graphql_requests.graphql_import_resolver import resolve_imports


cart_fragment = resolve_imports("cart_fragment.graphql")

ADD_ITEM = gql(
    f"""
    {cart_fragment}

    mutation AddItem($command: InputAddItemType!) {{
        addItem(command: $command) {{
            ...CartFragment
        }}
    }}
    """
)
