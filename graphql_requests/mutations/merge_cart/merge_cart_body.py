from gql import gql
from graphql_requests.graphql_import_resolver import resolve_imports


cart_fragment = resolve_imports("cart_fragment.graphql")

MERGE_CART = gql(
    f"""
    {cart_fragment}

    mutation MergeCart($command: InputMergeCartType!) {{
        mergeCart(command: $command) {{
            ...CartFragment
        }}
    }}
    """
)
