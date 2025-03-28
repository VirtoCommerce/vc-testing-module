from gql import gql
from graphql_requests.graphql_import_resolver import resolve_imports


customer_order_fragment = resolve_imports("customer_order_fragment.graphql")

CREATE_ORDER_FROM_CART = gql(
    f"""
    {customer_order_fragment}

    mutation CreateOrderFromCart($command: InputCreateOrderFromCartType!) {{
        createOrderFromCart(command: $command) {{
            ...CustomerOrderFragment
        }}
    }}
    """
)
