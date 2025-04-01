from gql import gql
from graphql_requests.graphql_import_resolver import resolve_imports

cart_fragment = resolve_imports("cart_fragment.graphql")

ADD_OR_UPDATE_CART_PAYMENT_BODY = gql(
    f"""
    {cart_fragment}

    mutation AddOrUpdateCartPayment($command: InputAddOrUpdateCartPaymentType!) {{
        addOrUpdateCartPayment(command: $command) {{
            ...CartFragment
        }}
    }}
    """
)
