from gql import gql
from graphql_requests.graphql_import_resolver import resolve_imports


bulk_cart_fragment = resolve_imports("bulk_cart_fragment.graphql")

ADD_BULK_ITEMS_CART = gql(
    f"""
    {bulk_cart_fragment}

    mutation AddBulkItemsCart($command: InputAddBulkItemsType!) {{
        addBulkItemsCart(command: $command) {{
            ...BulkCartFragment
        }}
    }}
    """
)
