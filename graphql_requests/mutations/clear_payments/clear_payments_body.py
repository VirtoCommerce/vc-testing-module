from gql import gql
from graphql_requests.graphql_import_resolver import resolve_imports


cart_fragment = resolve_imports("cart_fragment.graphql")

CLEAR_PAYMENTS = gql(
    f"""
    {cart_fragment}

    mutation ClearPayments($command: InputClearPaymentsType!) {{
        clearPayments(command: $command) {{
            ...CartFragment
        }}
    }}
    """
)
